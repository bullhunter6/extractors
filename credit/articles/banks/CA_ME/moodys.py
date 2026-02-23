import requests
from bs4 import BeautifulSoup
from dateutil import parser
from utils.check import filter_articles_by_region_2
from utils.keywords import COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS
from utils.db import save_article

def moodys_news():
    url = "https://www.moodys.com/web/en/us/insights/all/jcr:content/root/container/container_25347621/filter_container_cop.result-set.html?p=1&topic=((content-type/article))"

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        base_url = "https://www.moodys.com"
        cards = soup.find_all('div', class_='card-body')

        for card in cards:
            title = card.find('h5').get_text(strip=True) if card.find('h5') else None
            date = card.find('span', class_='card-date').get_text(strip=True) if card.find('span', class_='card-date') else None
            link_tag = card.find('a')
            link = base_url + link_tag['href'] if link_tag and 'href' in link_tag.attrs else None
            formatted_date = parser.parse(date).strftime("%Y-%m-%d")
            if not title or not link:
                continue

            content_response = requests.get(link, headers=headers)
            if content_response.status_code != 200:
                continue

            content_soup = BeautifulSoup(content_response.text, 'html.parser')
            article_div = content_soup.find('div', class_='text-article text')

            if article_div:
                content = []
                for element in article_div.find_all(['h5', 'p']):
                    content.append(element.get_text(strip=True))
                content = '\n\n'.join(content)
                region, keywords = filter_articles_by_region_2(title, content, COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS)

                if keywords:
                    articles_data = ({
                        "title": title,
                        "date": formatted_date,
                        "link": link,
                        "content": content,
                        "source": "moodys",
                        "region": region,
                        "sector": "banks",
                        "keywords": keywords,
                    })
                    save_article(articles_data)
                    articles.append(articles_data)

        

        return articles