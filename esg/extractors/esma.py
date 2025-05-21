import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.check import is_esg_related
import logging
from utils.db_utils import save_article

def esma_articles():
    url = "https://www.esma.europa.eu/press-news/esma-news"
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'cck1=%7B%22cm%22%3Atrue%2C%22all1st%22%3Atrue%2C%22closed%22%3Afalse%7D',
    'priority': 'u=0, i',
    'referer': 'https://www.esma.europa.eu/press-news/esma-news',
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

    response = requests.post(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    content_wrapper = soup.find("div", class_="views-infinite-scroll-content-wrapper")

    if content_wrapper:
        news_cards = content_wrapper.find_all("div", class_="news-contentcard")
        
        for card in news_cards:
            title_tag = card.find("span", class_="field--name-title")
            date_tag = card.find("div", class_="search-date")
            summary_tag = card.find("div", class_="field--name-field-news-introduction")
            
            if title_tag and date_tag and summary_tag:
                title = title_tag.get_text(strip=True)
                date_str = date_tag.get_text(strip=True)
                date = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
                link_tag = card.find("a", href=True)
                link = f"https://www.esma.europa.eu{link_tag['href']}" if link_tag else "No link available"
                response = requests.get(link, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                content = []
                content_section = soup.find("div", class_="node__content")
                if content_section:
                    paragraphs = content_section.find_all("p")
                    for paragraph in paragraphs:
                        content.append(paragraph.get_text(strip=True))
                article_text = "\n\n".join(content)
                
                matched_keywords = is_esg_related(title, article_text)
                if not matched_keywords:
                    logging.debug(f"Skipping non-relevant article: {title}")
                    continue
                article_data = {
                    "title": title,
                    "date": date,
                    "url": link,
                    "summary": article_text,
                    "source": "ESMA",
                    "keywords": matched_keywords
                }
                save_article(article_data)
                articles.append(article_data)

    return articles
