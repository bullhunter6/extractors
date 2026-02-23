import requests
import json
from bs4 import BeautifulSoup
from utils.check import filter_articles_by_region_2
from utils.keywords import COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS
from utils.db import save_article
from dateutil import parser


def pwc_articles():
    url = "https://www.pwc.com/content/pwc/gx/en/research-insights/insights-library/jcr:content/root/container/content-free-container-1/section_2137231403/collection_v2.rebrand-filter-dynamic.html?currentPagePath=/content/pwc/gx/en/research-insights/insights-library&list=%7B%7D&page=0&searchText=&defaultImagePath=/content/dam/pwc/network/collection-fallback-images"

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        try:

            data = json.loads(response.text)

            articles_data = data.get("elements", [])
            articles = []

            for article in json.loads(articles_data):
                title = article.get("title")
                link = article.get("href")
                date = article.get("publishDate")
                formatted_date = parser.parse(date).strftime('%Y-%m-%d')


                full_content = ""

                response = requests.get(link)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    article_section = soup.find_all('div', class_='section container responsivegrid')
                    content_list = []

                    if article_section:
                        for section in article_section:
                            headers = section.find_all(['h1', 'h2', 'h5'])
                            paragraphs = section.find_all('p')
                            section_content = '\n\n'.join(tag.get_text(strip=True) for tag in (headers + paragraphs))
                            if section_content.strip():
                                content_list.append(section_content)
                        full_content = '\n\n'.join(content_list)

                if full_content:
                    region, keywords = filter_articles_by_region_2(title, full_content, COMMON_KEYWORDS, REGIONAL_KEYWORDS,RARE_KEYWORDS)
                    if keywords:
                        articles_info = ({
                            "title": title,
                            "link": link,
                            "date": formatted_date,
                            "content": full_content,
                            "region": region,
                            "keywords": keywords,
                            "sector": "banks",
                            "source": "PwC"
                        })
                        save_article(articles_info)
                        articles.append(articles_info)

            return articles
        except (ValueError, KeyError) as e:
            print(f"Error parsing response: {e}")
            return []