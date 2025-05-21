import feedparser
from datetime import datetime
import logging
import requests
from bs4 import BeautifulSoup
from utils.db_utils import save_article

logging.basicConfig(level=logging.DEBUG)

RSS_FEEDS = [
    "https://climate.ec.europa.eu/node/2/rss_en",
    "https://energy.ec.europa.eu/node/2/rss_en",
    "https://environment.ec.europa.eu/node/686/rss_en",
    "https://joint-research-centre.ec.europa.eu/node/2/rss_en",
    "https://eismea.ec.europa.eu/node/2/rss_en"
]

def fetch_full_article_summary(article_url):
    """Fetches and returns the full summary of an article from its URL."""
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'cck1=%7B%22cm%22%3Atrue%2C%22all1st%22%3Atrue%2C%22closed%22%3Afalse%7D',
        'priority': 'u=0, i',
        'referer': 'https://climate.ec.europa.eu/news-your-voice/news_en',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }


    response = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    content_div = soup.find('div', class_='ecl')
    if content_div:
        summary = content_div.get_text(separator='\n').strip()
    else:
        summary = "No summary found"
        logging.warning(f"Failed to retrieve summary for {article_url}")

    return summary

def fetch_articles_from_feed(feed_url):
    """Fetches articles from a single RSS feed URL."""
    articles = []
    feed = feedparser.parse(feed_url)

    for entry in feed.entries:
        title = entry.get("title", "No Title")
        link = entry.get("link", "No Link")

        description = entry.get("description", "No Description")

        published = entry.get("published")
        if published:
            try:
                date_obj = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %z")
                formatted_date = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                logging.warning(f"Skipping article '{title}' due to invalid date format: {published}")
                formatted_date = "Unknown Date"
        else:
            formatted_date = "Unknown Date"
        full_summary = fetch_full_article_summary(link)

        article_data = {
            "title": title,
            "date": formatted_date,
            "url": link,
            "summary": full_summary if full_summary else description,
            "source": "European Commission",
            "keywords": "No Keywords"
        }
        save_article(article_data)
        articles.append(article_data)

    return articles

def ec_articles():
    """Extracts articles from all provided RSS feeds."""
    all_articles = []
    for feed_url in RSS_FEEDS:
        logging.info(f"Fetching articles from feed: {feed_url}")
        articles = fetch_articles_from_feed(feed_url)
        all_articles.extend(articles)
    
    return all_articles

