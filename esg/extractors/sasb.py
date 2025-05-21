import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.db_utils import save_article

def fetch_full_article_summary(article_url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'wp-wpml_current_language=en-gb',
        'priority': 'u=0, i',
        'referer': 'https://sasb.ifrs.org/blog/',
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
    content = ""
    article_content_div = soup.find('div', class_='article prose')
    if article_content_div:
        paragraphs = article_content_div.find_all('p')
        for paragraph in paragraphs:
            content += paragraph.get_text(strip=True) + "\n"

    return content

def sasb_articles():
    url = "https://sasb.ifrs.org/blog/"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'wp-wpml_current_language=en-gb',
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
    articles = []

    for item in soup.find_all('div', class_='list-item'):
        title = item.find('a', class_='title desktop').get_text(strip=True)

        article_url = item.find('a', class_='title desktop')['href']

        date_str = item.find('div', class_='date').get_text(strip=True)
        date_obj = datetime.strptime(date_str, '%B %d, %Y')
        formatted_date = date_obj.strftime('%Y-%m-%d')

        summary = item.find('p', class_='text').get_text(strip=True)
        full_summary = fetch_full_article_summary(article_url)

        articles_data =  {
            'title': title,
            'date': formatted_date,
            'url': article_url,
            'summary': full_summary,
            'source': 'SASB',
            'keywords': "No Keywords"
        }
        save_article(articles_data)
        articles.append(articles_data)

    return articles