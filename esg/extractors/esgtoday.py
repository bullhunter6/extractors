import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from utils.db_utils import save_article

logging.basicConfig(level=logging.DEBUG)

def esgtoday_articles():
    url = "https://www.esgtoday.com/category/esg-news/"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles_container = soup.find('div', id='loops-wrapper')
    if not articles_container:
        logging.error("Failed to find articles container.")
        return []

    article_elements = articles_container.find_all('article', class_='post')
    articles = []

    for article in article_elements:

        title_tag = article.find('h2', class_='post-title entry-title')
        title = title_tag.text.strip() if title_tag else "No Title"

        link_tag = title_tag.find('a') if title_tag else None
        full_link = link_tag['href'] if link_tag else "No Link"

        date_tag = article.find('time', class_='post-date')
        date_str = date_tag['datetime'] if date_tag else None
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%Y-%m-%d")
        except (TypeError, ValueError):
            logging.warning(f"Skipping article '{title}' due to invalid date format: {date_str}")
            continue
        response = requests.get(full_link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='entry-content')
        if content_div:
            full_content = content_div.get_text(separator='\n').strip()
        else:
            full_content = "No content found"
            logging.warning(f"Failed to retrieve content for {full_link}")
        category_tags = article.find_all('a', class_='post-category')
        keywords = ', '.join(tag.text for tag in category_tags) if category_tags else "No Keywords"
        article_data = {
            "title": title,
            "date": formatted_date,
            "url": full_link,
            "summary": full_content,
            "source": "ESG Today",
            "keywords": "No Keywords"
        }
        save_article(article_data)
        articles.append(article_data)

    return articles
