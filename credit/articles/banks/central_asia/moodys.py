from utils.db import save_article
from dateutil import parser
import feedparser

def fi_ca_moodys():
    rss_feed_url = "https://www.moodys.com/rss.aspx?id=609b1bf8-c63d-418f-bf40-aeaac8421f5e&alert_id=59717&type=custom"
    feed = feedparser.parse(rss_feed_url)
    articles = []

    for entry in feed.entries:
        title = entry.title
        if "global".lower() in title.lower():
            print(f"Skipping global article: {title}")
            continue
        link = entry.link
        content = entry.description
        pubDate = entry.published
        date = parser.parse(pubDate).strftime("%Y-%m-%d")
        article = {
            'title': title,
            'link': link,
            'content': content,
            'date': date,
            'source': 'moodys',
            'region': 'CentralAsia',
            'sector': 'banks',
            'keywords': None,
        }
        save_article(article)
        articles.append(article)

    return articles