import yfinance as yf
from textblob import TextBlob
from datetime import datetime, timedelta
import pytz


def get_sentiment(symbol):
    ticker = yf.Ticker(symbol)
    raw_news = ticker.news
    eastern = pytz.timezone('US/Eastern')
    now = datetime.now(eastern)

    headlines = []

    for n in raw_news:
        title = n.get('title') or n.get('content', {}).get('title')
        # Extract direct click-through URL
        link = n.get('content', {}).get('clickThroughUrl') or n.get('link')
        if isinstance(link, dict):
            link = link.get('url')
        if not link:
            link = "https://finance.yahoo.com"

        source_raw = n.get('publisher') or n.get('content', {}).get('provider', {}).get('displayName', 'YF')
        source_tag = "MW" if "Watch" in source_raw else "CNBC" if "CNBC" in source_raw else "YF"

        if not title: continue

        pub_ts = n.get('providerPublishTime') or n.get('content', {}).get('pubDate')
        try:
            pub_time = datetime.fromtimestamp(pub_ts, pytz.utc).astimezone(eastern)
        except:
            pub_time = now

        sentiment = TextBlob(title).sentiment.polarity

        if pub_time > now - timedelta(hours=24):
            headlines.append({
                "title": title,
                "url": link,
                "time": pub_time.strftime("%I:%M %p ET"),
                "source": source_tag,
                "sentiment": sentiment
            })

    summary = f"Catalyst: {headlines[0]['title'][:60]}..." if headlines else "Internal price action driving bias."
    return round(sum([h['sentiment'] for h in headlines[:5]]), 2), headlines[:5], summary