import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.db_utils import save_pub

def unepfi_pub():
    url = "https://www.unepfi.org/category/publications/"
    headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }
    response = requests.request("GET", url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    publication_articles = soup.find_all('article', class_='d-sm-flex align-content-stretch justify-content-left')
    articles = []
    for article in publication_articles:
        title = article.find('h5').text.strip()
        summary = article.find('p').text.strip()
        link = article.find('a')['href']
        source = 'UNEP FI'
        image_url = article.find('img')['src']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        article_data = {
            'title': title,
            'summary': summary,
            'link': link,
            'source': source,
            'image_url': image_url,
            'date': date
        }
        save_pub(article_data)
        articles.append(article_data)
    return articles