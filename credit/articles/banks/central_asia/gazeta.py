import feedparser
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from utils.check import is_ca_related
from utils.keywords import CA_KEYWORDS
from utils.db import save_article
import logging

def extract_article_content(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "language=en; language_chosen=1; session=cae15321c68da435b103c6c83b6dc965",
        "priority": "u=0, i",
        "referer": "https://www.gazeta.uz/en/economy",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        content_block = soup.find("div", itemprop="articleBody")
        paragraphs = content_block.find_all("p")
        content = "\n".join([p.get_text(strip=True) for p in paragraphs])

        return content

def gazeta_bk():
    url = "https://www.gazeta.uz/en/rss/"

    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        date = entry.published
        content = extract_article_content(link)
        formatted_date = parse(date).strftime("%Y-%m-%d")
        matched_keywords = is_ca_related(title, content, CA_KEYWORDS)
        if not matched_keywords:
            logging.debug(f"Skipping non-relevant article: {title}")
            continue

        articles_info = ({
            'date': formatted_date,
            'title': title,
            'link': link,
            'content': content,
            'source': 'Gazeta',
            'keywords': matched_keywords,
            'region': 'CentralAsia',
            'sector': 'banks',
        })
        articles.append(articles_info)
        save_article(articles_info)
    return articles


