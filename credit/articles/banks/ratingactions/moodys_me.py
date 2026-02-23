import requests
from utils.check import me_related
from utils.db import save_article
from dateutil import parser
import feedparser

def fi_ra_me_moodys():
    rss_feed_url = "https://www.moodys.com/rss.aspx?id=609b1bf8-c63d-418f-bf40-aeaac8421f5e&alert_id=59710&type=custom"
    feed = feedparser.parse(rss_feed_url)
    articles = []

    for entry in feed.entries:
        title = entry.title
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
            'region': 'MiddleEast',
            'sector': 'banksRACS',
            'keywords': None,
        }
        save_article(article)
        articles.append(article)

    return articles