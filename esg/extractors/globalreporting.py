import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.db_utils import save_article

def globalreporting_articles():
    url = "https://www.globalreporting.org/news/news-center/"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'ASP.NET_SessionId=wkeksjszibul33l12frcwv4l; CookieConsent={stamp:%27g+kyPjm77zqCO1tbfNzzz+MyyEjbZKCzOHwhehjPQEcixlysMoreNA==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1731480134808%2Cregion:%27ae%27}',
        'priority': 'u=0, i',
        'referer': 'https://www.globalreporting.org/news/news-center/',
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

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles_section = soup.find('div', class_='news')
    articles = []

    for item in articles_section.find_all('div', class_='list-card__item'):
        title = item.find('h4').get_text(strip=True)
        summary = item.find('p').get_text(strip=True)
        date_str = item.find('span', class_='list-card__date').get_text(strip=True)
        relative_url = item.find('a')['href']
        article_url = "https://www.globalreporting.org" + relative_url
        date_obj = datetime.strptime(date_str, '%d %b %Y')
        formatted_date = date_obj.strftime('%Y-%m-%d')

        response = requests.get(article_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = ""
        for div in soup.find_all(['div'], class_=['content__text', 'content__quote']):
            paragraphs = div.find_all('p')
            for paragraph in paragraphs:
                content += paragraph.get_text(strip=True) + "\n"

        articles_data = {
            'title': title,
            'summary': content,
            'date': formatted_date,
            'url': article_url,
            'source': 'Global Reporting Initiative',
            "keywords": "No Keywords"
        }
        save_article(articles_data)
        articles.append(articles_data)

    return articles