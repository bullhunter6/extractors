import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from utils.db_utils import save_article

logging.basicConfig(level=logging.DEBUG)

def unepfi_articles():
    url = "https://www.unepfi.org/tag/top-news/"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=r9oeunf9o04jvbein8upj9pc5k',
        'Referer': 'https://www.unepfi.org/tag/top-news/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
        }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []

    article_elements = soup.select('section.publications-list article')
    for article in article_elements:
        title_tag = article.find('h3', class_='mb-3')
        title = title_tag.get_text(strip=True) if title_tag else "No Title"
        link_tag = title_tag.find_parent('a')
        link = link_tag['href'] if link_tag else "No Link"
        
        date_tag = article.find('span', class_='date')
        date_str = date_tag.get_text(strip=True) if date_tag else None
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%d %B %Y")
                formatted_date = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                logging.warning(f"Skipping article '{title}' due to invalid date format: {date_str}")
                formatted_date = "Unknown Date"
        else:
            formatted_date = "Unknown Date"

        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='post-content')
        if not content_div:
            logging.error("No content found in 'post-content' div.")
            return None
        paragraphs = content_div.find_all(['p', 'h5', 'ol', 'ul'])
        article_content = "\n\n".join(paragraph.get_text(strip=True) for paragraph in paragraphs)


        article_data = {
            "title": title,
            "date": formatted_date,
            "url": link,
            "summary": article_content,
            "source": "UNEP FI",
            "keywords": "No Kewords",
        }


        save_article(article_data)
        articles.append(article_data)

    return articles

