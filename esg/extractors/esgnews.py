import feedparser
from datetime import datetime
import logging
from utils.db_utils import save_article
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)

RSS_FEEDS = [
    'https://esgnews.com/category/sustainable-finance/feed/',
    'https://esgnews.com/esg-environment/feed/',
    'https://esgnews.com/esg-latin-america/feed/',
    'https://esgnews.com/esg-newsletter/feed/',
    'https://esgnews.com/force-for-good/feed/',
    'https://esgnews.com/category/digital-assets/feed/',
    'https://esgnews.com/category/esg-funds/feed/',
    'https://esgnews.com/esg-international/feed/',
    'https://esgnews.com/feed/',
    'https://esgnews.com/esg-business/feed/'
]

def parse_html_content(html_content):
    """Cleans and extracts text content from HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator='\n').strip()

def fetch_articles_from_feed(feed_url):
    """Fetches articles from a single RSS feed URL."""
    articles = []
    feed = feedparser.parse(feed_url)

    for entry in feed.entries:
        title = entry.get("title", "No Title")
        link = entry.get("link", "No Link")

        published = entry.get("published")
        if published:
            try:
                date_obj = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %z")
                formatted_date = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                logging.warning(f"Skipping article '{title}' due to invalid date format: {published}")
                continue
        else:
            formatted_date = "Unknown Date"

        summary = entry.get("description", "No Summary")
        full_content_html = entry.get("content:encoded", summary)
        full_content = parse_html_content(full_content_html)

        categories = [tag.term for tag in entry.tags] if "tags" in entry else []
        keywords = ', '.join(categories) if categories else "No Keywords"

        article_data = {
            "title": title,
            "date": formatted_date,
            "url": link,
            "summary": full_content,
            "source": "ESG News",
            "keywords": "No Keywords"
        }

        save_article(article_data)
        articles.append(article_data)

    return articles

def esgnews_articles():
    """Extracts articles from all provided RSS feeds."""
    all_articles = []
    for feed_url in RSS_FEEDS:
        logging.info(f"Fetching articles from feed: {feed_url}")
        articles = fetch_articles_from_feed(feed_url)
        all_articles.extend(articles)
    
    return all_articles


