import requests
from bs4 import BeautifulSoup
from dateutil import parser
import re
from utils.check import filter_articles_by_region_2
from utils.keywords import COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS
from utils.db import save_article



def fetch_article_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        content = ""
        target_divs = soup.find_all('div', class_='cmp-text')
        if target_divs:
            for div in target_divs:
                paragraphs = div.find_all('p')
                for p in paragraphs:
                    content += p.get_text() + "\n"

        script_tag = soup.find('script', string=re.compile(r"dataLayer\.page"))
        publish_date = None
        fromatted_date = None
        if script_tag:
            match = re.search(r'"publishDate"\s*:\s*"([^"]+)"', script_tag.string)
            if match:
                publish_date = match.group(1)
                fromatted_date = parser.parse(publish_date).strftime("%Y-%m-%d")

        return content.strip(), fromatted_date
    except Exception as e:
        print(f"Error fetching content for URL {url}: {e}")
        return None, None

def deloitte():
    url = "https://www2.deloitte.com/us/en/insights.html"
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        article_containers = soup.find_all('div', class_='cmp-di-promo-container__content')

        articles = []

        for container in article_containers:
            promos = container.find_all('a', class_='cmp-di-promo-tracking')
            for promo in promos:
                title = promo.find('h3', class_='cmp-di-promo__content__title')
                description = promo.find('p', class_='mb-1')
                article_type = promo.find('div', class_='cmp-di-promo__content__type')
                link = promo.get('href')

                title = title.get_text(strip=True) if title else None
                description = description.get_text(strip=True) if description else None
                article_type = article_type.get_text(strip=True) if article_type else None
                full_link = f"https://www2.deloitte.com{link}" if link and link.startswith('/') else link

                if title and full_link:
                    content, publish_date = fetch_article_content(full_link)
                    if content:
                        region, keywords = filter_articles_by_region_2(title, content, COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS)
                        if keywords:
                            articles_info = ({
                                "title": title,
                                "link": full_link,
                                "date": publish_date,
                                "content": content,
                                "region": region,
                                "keywords": keywords,
                                "sector": "banks",
                                "source": "Deloitte"
                            })
                            save_article(articles_info)
                            articles.append(articles_info)
        return articles

    except Exception as e:
        print(f"Error fetching articles from Deloitte: {e}")
        return []