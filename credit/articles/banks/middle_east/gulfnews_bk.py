import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.check import me_related
from utils.db import save_article
from utils.keywords import me_gf_KEYWORDS
import logging

def get_content(url):
    headers = {
        'Cookie': 'visid_incap_1101165=KI64tySQQr+wQXXM0IIeLza7RmcAAAAAQUIPAAAAAAAVUWhq3UM6ZlE5vDA6BeCD'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    title_element = soup.find('p', class_='ORiM7')
    title = title_element.get_text(strip=True) if title_element else "Title not found"
    date_element = soup.find('div', class_='Ubcaz')
    date_text = date_element.get_text(strip=True) if date_element else "Date not found"
    try:
        raw_date = date_text.replace("Last updated:", "").split("|")[0].strip()
        formatted_date = datetime.strptime(raw_date, "%B %d, %Y").strftime("%Y/%m/%d")
    except ValueError:
        formatted_date = "Invalid date format"

    content_elements = soup.find_all('div', class_='Iqx1L')
    content = "\n".join([paragraph.get_text(strip=True) for paragraph in content_elements])
    return formatted_date, content, title

def gulfnews_banks():
    url = "https://gulfnews.com/business/banking"
    headers = {
        'Cookie': 'visid_incap_1101165=KI64tySQQr+wQXXM0IIeLza7RmcAAAAAQUIPAAAAAAAVUWhq3UM6ZlE5vDA6BeCD'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('a', href=True)
    article_list = []
    for article in articles:
        title_1 = article.find('h2').get_text(strip=True) if article.find('h2') else None
        link = article['href'] if article['href'].startswith('/') else None
        if link:
            full_link = f"https://gulfnews.com{link}"

            date, content, detailed_title = get_content(full_link)
            final_title = title_1 if title_1 else detailed_title
            matched_keywords = me_related(final_title, content, me_gf_KEYWORDS)
            if not matched_keywords:
                logging.debug(f"Skipping non-relevant article: {final_title}")
                continue
            
            article_data = {
                'title': final_title,
                'link': full_link,
                'date': date,
                'content': content,
                'source': 'Gulf News',
                'region': 'MiddleEast',
                'sector': 'banks',
                'keywords': matched_keywords
            }
            
            save_article(article_data)
            article_list.append(article_data)
    
    return article_list