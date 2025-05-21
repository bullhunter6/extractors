import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.db_utils import save_article

def weform_articles():
    url = "https://www.weforum.org/press/"
    headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'Accept-Language': 'en-US,en;q=0.9',
      'Cache-Control': 'max-age=0',
      'Connection': 'keep-alive',
      'Cookie': 'mpDistinctId=cd3b86de-61c9-400a-9ab1-d76480a89b80; _web_session=U2IvbTIvd0NSR3lON3czTk5NdTJaQmlhbSswbmoyY2hpZWZKdSt2bUlPeTFpWGhzOWVIRGZkSmJ3WW9JdjN2akg1aDgxd2tGZUZpMXZFZTNUZXdsR0J2UWFZUjAyZ3Z1cUt4QnBxaXRpOHNpcFFiOHd6S2tOQnZOYUo2SGJud0pVblhKcWtLdFcxMVU0b3NlVm1DRFFnPT0tLUdSdUFsME9lT1VxOHY4MDZSQzhrUUE9PQ%3D%3D--b95d420e1a78b4f624552233c46a7f3ab9f56309; mp_6232aeb08818ee1161204a011ed8ad16_mixpanel=%7B%22distinct_id%22%3A%20%22cd3b86de-61c9-400a-9ab1-d76480a89b80%22%2C%22%24device_id%22%3A%20%2218ecc57fb8e1119-0e6d6dc1d393ac-26001a51-1bcab9-18ecc57fb8e1119%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22%24user_id%22%3A%20%22cd3b86de-61c9-400a-9ab1-d76480a89b80%22%2C%22platform%22%3A%20%22Public%20Site%22%2C%22%24search_engine%22%3A%20%22google%22%7D; _web_session=VmxTeXVrczV4ZC9jTmNBMEZHcVFsVjVidkhFNld3WDNKT0xhRUdHZFdJTm43dFNiUTUrMVEwVzhjc0hxYVU2WU5GNkh1NDNhSk14K3pSUW5RQkgzclZpYzVjUXcwOGxmR25YTlFQenM1clBHZFQ5MzJrb0dYb3IzeGtqcWFUczN4RnZRWjdQZ29LN3IzSm9ZL2oyTkdnPT0tLTRFK3QyeTNnZFR3ZGxZVk8vblhHOXc9PQ%3D%3D--563b77f0b871f0845f8636f1fc323835a87848d2',
      'If-None-Match': 'W/"5e2fd9f439a2324e6ebe2c72d30c60de"',
      'Referer': 'https://www.weforum.org/',
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
    for item in soup.find_all('div', class_='media-article'):
        title = item.find('a', class_='media-article__link').get_text(strip=True)

        relative_url = item.find('a', class_='media-article__link')['href']
        article_url = "https://www.weforum.org" + relative_url
        date_str = item.find_all('span', class_='caption')[1].get_text(strip=True)
        date_obj = datetime.strptime(date_str, '%d %b %Y')
        formatted_date = date_obj.strftime('%Y-%m-%d')


        response = requests.get(article_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = ""
        for block in soup.find_all('div', class_=['st__content-block--text', 'st__content-block--list']):
            if block.name == 'div' and block.find('p'):
                paragraphs = block.find_all('p')
                for paragraph in paragraphs:
                    content += paragraph.get_text(strip=True) + "\n"
            elif block.name == 'div' and block.find('ul'):
                list_items = block.find_all('li')
                for item in list_items:
                    content += "- " + item.get_text(strip=True) + "\n"


        articles_data = {
            'title': title,
            'date': formatted_date,
            'url': article_url,
            'summary': content,
            'source': 'World Economic Forum',
            'keywords': 'No keywords'
        }
        save_article(articles_data)
        articles.append(articles_data)
    return articles