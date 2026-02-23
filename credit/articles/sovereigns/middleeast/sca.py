import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from utils.check import me_related
from utils.keywords import me_sca_KEYWORDS
from utils.db import save_article

sovereign_keywords =[
   "IPO","sovereign rating","UAE", "United Arab Emirates", "Saudi Arabia", "GCC countries", "GCC", "Kuwait", "Oman", "Bahrein", "Qatar", "Dubai", "Abu Dhabi","KSA", "saudi", 
    "Middle east", "RAK","Sharjah", "Ras Al Khamiah","Gulf Cooperation Council","Persian Gulf", "Islamic Cooperation", "Arab League","Muscat","Red Sea", "Yemen", "Jordan", 
    "MENA", "OPEC", "Organization of the Petroleum Exporting Countries", "Arabic Gulf", "Arabian Sea",
    
    "Finance system","local goverment","goverment","goverment bonds","goverment spending","goverment budget",
    "goverment deficit","goverment surplus","goverment revenue","goverment expenditure","goverment fiscal policy","goverment monetary policy","goverment stimulus","goverment recovery",
    "goverment growth","goverment outlook","goverment impact","goverment contraction","goverment indicators","goverment rate cut","goverment mortgage","goverment mortgages",
    "goverment interest rate","goverment interest rates","goverment central bank","goverment central banks","goverment monetary policy","goverment fiscal policy",
    "goverment budget","goverment budgets","goverment deficit","goverment deficits","goverment government debt","goverment debt to GDP","goverment GDP","goverment GDP growth",
    "goverment economy","goverment economic","goverment economic growth","goverment economic outlook","goverment economic recovery","goverment economic stimulus",
    "goverment economic stimulus package","goverment economic impact","goverment economic contraction","goverment economic indicators","goverment rate cut",
    "goverment mortgage","goverment mortgages",'interest rate','interest rates','monetary policy','fiscal policy','goverment budget','goverment budgets','deficit',
    'deficits','government debt','debt to GDP','GDP','GDP growth',"economic growth","economic outlook","economic recovery","economic stimulus",
    "economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgage","mortgages","sukuk","economic growth","economic outlook",
    "economic recovery","economic stimulus","economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgage","mortgages",
]

def clean_summary(html_summary):
    soup = BeautifulSoup(html_summary, 'html.parser')
    for tag in soup.find_all(True):
        tag.attrs = {}
    text = soup.get_text(separator=' ', strip=True)
    return text

def sca_sov():
    url = "https://www.sca.gov.ae/RSS/News.ashx?lang=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item')

    results = []
    for item in items:
        title = item.find('title').text.strip()
        date = item.find('pubDate').text.strip()
        summary_html = item.find('description').text.strip()
        summary = clean_summary(summary_html)
        url = item.find('link').text.strip()

        matched_keywords = me_related(title, summary, sovereign_keywords)
        if not matched_keywords:
            logging.debug(f"Skipping non-relevant article: {title}")
            continue

        try:
            parsed_date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z").strftime('%Y-%m-%d')
            logging.debug(f"Parsed date: {parsed_date} for article: {title}")
        except ValueError:
            logging.warning(f"Could not parse date: {date} for article: {title}")
            continue

        article_data = {
            'title': title,
            'date': parsed_date,
            'content': summary,
            'link': url,
            'source': 'SCA',
            'keywords': ', '.join(matched_keywords),
            'region': 'MiddleEast',
            'sector': 'sovereigns'
        }
        save_article(article_data)
        results.append(article_data)


    return results