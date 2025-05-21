import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.db_utils import save_article

def bcg_articles():
    url = "https://www.bcg.com/search?f7=00000171-f179-d0c2-a57d-fbfd3be20000&s=1&q=ESG%20%26%20Sustainable%20Investing%20and%20Finance"

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '...',
        'priority': 'u=1, i',
        'referer': 'https://www.bcg.com/search?f7=00000171-f179-d0c2-a57d-fbfd3be20000&s=1&q=ESG+%26+Sustainable+Investing+and+Finance',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles_container = soup.find('div', {'data-qa': 'hits'})
        
        if articles_container:
            articles = []
            for section in articles_container.find_all('section', class_='search-result'):
                title_tag = section.find('h2', class_='title')
                title = title_tag.text.strip() if title_tag else 'No title available'
                link_tag = title_tag.find('a') if title_tag else None
                link = link_tag['href'] if link_tag else 'No link available'
                date_tag = section.find('p', class_='subtitle')
                date = date_tag.text.strip() if date_tag else 'No date available'
                try:
                    formatted_date = datetime.strptime(date, "%B %d, %Y").strftime("%Y/%m/%d")
                except ValueError:
                    formatted_date = "Invalid date format"
                intro_tag = section.find('p', class_='intro')
                intro = intro_tag.text.strip() if intro_tag else 'No intro available'
                response = requests.get(link, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    content_div = soup.find('div', class_='text-panel')
                    paragraphs = content_div.find_all('p') if content_div else []
                    summary = ' '.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                articles_data =({
                    'title': title,
                    'url': link,
                    'date': formatted_date,
                    'summary': summary,
                    'source': 'BCG',
                    'keywords': None
                })
                save_article(articles_data)
                articles.append(articles_data)
            return articles