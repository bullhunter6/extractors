import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from utils.db_utils import save_article
from utils.check import is_esg_related
import logging

def fca_articles():
    url = "https://www.fca.org.uk/news/rss.xml"
    response = requests.get(url)
    root = ET.fromstring(response.content)
    articles = []
    for item in root.findall(".//item"):
        title = item.find("title").text.strip() if item.find("title") is not None else "No title"
        link = item.find("link").text.strip() if item.find("link") is not None else "No link"
        description = item.find("description").text.strip() if item.find("description") is not None else "No description"
        pub_date_raw = item.find("pubDate").text.strip() if item.find("pubDate") is not None else "No date"
        try:
            pub_date = datetime.strptime(pub_date_raw.split(" -")[0], "%A, %B %d, %Y").strftime("%Y-%m-%d")
        except ValueError:
            pub_date = "Invalid date format"

        matched_keywords = is_esg_related(title, description)
        if not matched_keywords:
            logging.debug(f"Skipping non-relevant article: {title}")
            continue
        articles_data = ({
            "title": title,
            "url": link,
            "summary": description,
            "date": pub_date,
            "source": "FCA",
            "keywords": matched_keywords
        })
        save_article(articles_data)
        articles.append(articles_data)

    return articles