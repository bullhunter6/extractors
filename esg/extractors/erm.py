import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from utils.db_utils import save_article

logging.basicConfig(level=logging.INFO)

def erm_articles():
    url = "https://www.erm.com/about/news"
    base_url = "https://www.erm.com"
    headers = {
        'accept': 'text/html, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'TiPMix=56.05430269384072; x-ms-routing-name=self; ASP.NET_SessionId=fwpdeq5yc0e4zt0ssop22zkx; .EPiForm_BID=8832de6d-6012-4bb7-9607-865f7c4e9a7f; .EPiForm_VisitorIdentifier=8832de6d-6012-4bb7-9607-865f7c4e9a7f:; __RequestVerificationToken=oriL7MeijUPlMbyMiGlV0PSgRhl4PKx9gqJ-YA6eS12bCCvWqO9rUtA9f2rU9c3WN-tXWcU6ttvPFPDkT8LUj2JgZWVCcOGt_-buVX0oxT01; ARRAffinity=991c0538760a6c5a62f9e2186ee65fe1891aebea99e61d85f6c19a961c61e4e7; ARRAffinitySameSite=991c0538760a6c5a62f9e2186ee65fe1891aebea99e61d85f6c19a961c61e4e7; OptanonAlertBoxClosed=2024-11-12T09:28:55.102Z; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Nov+12+2024+13%3A30%3A24+GMT%2B0400+(Gulf+Standard+Time)&version=202306.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=b40129e8-069f-4c2b-a01b-154d8d31de44&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1&geolocation=AE%3BDU&AwaitingReconsent=false',
        'priority': 'u=1, i',
        'referer': 'https://www.erm.com/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    items_container = soup.find('div', id='items-container')
    if not items_container:
        print("Error: 'items-container' not found on the page.")
        return []
    
    articles_elements = items_container.find_all('div', class_='list-result')
    articles = []

    for article in articles_elements:
        title_tag = article.find('p', class_='result-teaser')
        title = title_tag.text.strip() if title_tag else "No Title"

        date_str_tag = article.find('div', class_='results-date')
        date_str = date_str_tag.text.strip() if date_str_tag else None

        if not date_str:
            logging.warning(f"Article '{title}' skipped due to missing date.")
            continue

        try:
            date_obj = datetime.strptime(date_str, "%d %B %Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
        except ValueError:
            logging.warning(f"Article '{title}' skipped due to invalid date format: {date_str}")
            continue

        link_tag = article.find('a', class_='result-link')
        relative_link = link_tag['href'] if link_tag else ""
        full_link = base_url + relative_link if relative_link else "No Link"

        article_response = requests.get(full_link, headers=headers)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        content_div = article_soup.find('div', class_='wysiwyg main-content')
        content = content_div.get_text(separator='\n').strip() if content_div else "No Content"

        article_data = {
            "title": title,
            "date": formatted_date,
            "url": full_link,
            "summary": content,
            "source": "ERM",
            "keywords": "No Keywords"
        }
        save_article(article_data)
        articles.append(article_data)

    return articles