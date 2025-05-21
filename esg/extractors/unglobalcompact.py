import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from utils.db_utils import save_article

logging.basicConfig(level=logging.INFO)

def unglobalcompact_articles():
    url = "https://unglobalcompact.org/news/press-releases"

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': '_gd_session=df1a25e7-3847-4117-88ca-0cc77c3adc8d; _ungc_session=U2TPup0KgMMQDLB8%2FyTzlFS37URDVH6lqLZeMHg7N6ui2KC6Iaf4UnZNWuw0OMCs%2BZPZ%2BwLwSxy080YtAKhHFQ0fyYn9Kq0u08zmSsaEnjIRMxnoi21whGYOz3hm9FJxdtThrCv0fISOoEfz3dPu5QurvaWkAML8UbaIRVIT96HEN2EY6bb028ThGDOqtJ5Z7nKPINsq3mDdY8PlITzIHIB6Gk%2FxFhrNBqcEYb4betu5KGNB7VCGjlf80dYiDIqC5dWtJATWTzWnIAQ6okHG4z5P6c66--I3XVw2Utv0xg%2B8te--nJVJqw2fosYj2Cr0m7AYqw%3D%3D; _gd_visitor=4dda1f2a-dac7-48c8-8bf0-6579371c1ac1; _ungc_session=pniN1EeoQ9CGVMOrGg5M1pJIdBAedHD93QjD8vb%2Ba8wBgQ84w29%2BWp%2BXmrhuU%2FSpszBxVtpEyS3jg79iF7jNZ%2BlL4UQr58UUnb0fkouN7SSs730T81TEtnwQUCB5UGy2p%2FyOG4jc1W4wbQddJ3B9cWpTbwEZY6NXUatRVKsFwOtYH6GV5CiQNgFbln%2BPVH7acv5kju72cCMyAldyvUaKEtphZExZmus7OWnA2u2Y1chUj1gpkHADWW1uIwBLvVGrgVUcoT%2BUr6eUSd34nkiyJVeKxSZo--wVtnkZJUHi1AlL%2FL--CVfnXvLq0jf8ieWZcqoMjA%3D%3D',
        'if-none-match': 'W/"098a77164978ea2e73d83747996cfd31"',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.select("section.main-content-section .news-item")
    articles_data_list = []

    for article in articles:
        title = article.h1.get_text(strip=True)

        date_str = article.find('time').get_text(strip=True)
        if not date_str:
            logging.warning(f"Article '{title}' skipped due to missing date.")
            continue

        try:
            date_obj = datetime.strptime(date_str, "%d-%b-%Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
        except ValueError:
            logging.warning(f"Article '{title}' skipped due to invalid date format: {date_str}")
            continue

        link = "https://unglobalcompact.org" + article.h1.a['href']

        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        content_section = soup.select_one("section.main-content-body")
        if content_section:
            full_summary = " ".join(p.get_text(strip=True) for p in content_section.find_all("p"))

        articles_data = {
            "title": title,
            "date": formatted_date,
            "summary": full_summary,
            "url": link,
            "source": "UN Global Compact",
            "keywords": "No Keywords"
        }
        save_article(articles_data)
        articles_data_list.append(articles_data)
    
    return articles_data_list
