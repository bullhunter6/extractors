import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from utils.db_utils import save_article

logging.basicConfig(level=logging.DEBUG)

def greenbiz_articles():
    url = "https://trellis.net/articles/"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'PHPSESSID=fd31b24115b1b5c8a47f5c880ccc024f; OptanonAlertBoxClosed=2024-11-12T09:29:57.485Z; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Nov+12+2024+15%3A52%3A05+GMT%2B0400+(Gulf+Standard+Time)&version=202407.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=da0b1919-0895-468a-8d85-03907bda42f2&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0002%3A1%2CC0001%3A1&intType=1&geolocation=AE%3BDU&AwaitingReconsent=false',
        'priority': 'u=0, i',
        'referer': 'https://trellis.net/articles/',
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
    section = soup.find('section', class_='md:py-16 sm:py-12 py-8')
    if not section:
        logging.error("Failed to find articles section.")
        return []
    article_elements = section.find_all('div', class_='tease-post')
    articles = []

    for article in article_elements:
        title_tag = article.find('h2', class_='sm:text-[32px] text-2xl font-semibold leading-tight')
        title = title_tag.get_text(strip=True) if title_tag else "No Title"
        
        link_div = article.find('div', class_='flex items-center sm:max-w-[40%] lg:pl-8')
        link_tag = link_div.find('a', href=True) if link_div else None
        link = link_tag['href'] if link_tag else "No Link"

        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='post-content')
        if content_div:
            full_content = content_div.get_text(separator='\n').strip()
        else:
            full_content = "No content found"
            logging.warning(f"Failed to retrieve content for {link}")

        date_tag = article.find('time', class_='text-color font-medium text-sm')
        date_str = date_tag['datetime'] if date_tag else None
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                formatted_date = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                logging.warning(f"Skipping article '{title}' due to invalid date format: {date_str}")
                formatted_date = "Unknown Date"
        else:
            formatted_date = "Unknown Date"


        article_data = {
            "title": title,
            "date": formatted_date,
            "url": link,
            "summary": full_content,
            "source": "GreenBiz",
            "keywords": "No Keywords"
        }

        save_article(article_data)
        articles.append(article_data)

    return articles

