import requests
from bs4 import BeautifulSoup
from utils.check import is_ca_related
import logging
from utils.db import save_article
from dateutil import parser
from datetime import datetime

sovereign_keywords =[
    "sovereign","sovereign rating",
    
    "Asia and Pacific", "Asia-Invest Bank", "Asian Development Bank","private sector","public sector",
    
    'energy sector',"Masdar",'National Fund','ADNOC','green economy','Abu Dhabi',"Dubai","UAE",'Senate of Uzbekistan',

    "privatisation","Finance system","local goverment","goverment","goverment bonds","goverment spending","goverment budget",
    "goverment deficit","goverment surplus","goverment revenue","goverment expenditure","goverment fiscal policy","goverment monetary policy","goverment stimulus","goverment recovery",
    "goverment growth","goverment outlook","goverment impact","goverment contraction","goverment indicators","goverment rate cut","goverment mortgage","goverment mortgages",
    "goverment interest rate","goverment interest rates","goverment central bank","goverment central banks","goverment monetary policy","goverment fiscal policy",
    "goverment budget","goverment budgets","goverment deficit","goverment deficits","goverment government debt","goverment debt to GDP","goverment GDP","goverment GDP growth",
    "goverment economy","goverment economic","goverment economic growth","goverment economic outlook","goverment economic recovery","goverment economic stimulus",
    "goverment economic stimulus package","goverment economic impact","goverment economic contraction","goverment economic indicators","goverment rate cut",
    "goverment mortgage","goverment mortgages",'interest rate','interest rates','monetary policy','fiscal policy','goverment budget','goverment budgets','budget deficit',
    'deficits','government debt','debt to GDP','GDP','GDP growth',"economy","economic growth","economic outlook","economic recovery","economic stimulus",
    "economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgage","mortgages","sukuk","economic growth","economic outlook",
    "economic recovery","economic stimulus","economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgage","mortgages","investments"
]

def get_content_uz(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=0, i",
        "referer": "https://www.uzdaily.uz/en/section/1/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        content_block = soup.find("div", class_="content_body")
        paragraphs = content_block.find_all("p")
        content = "\n".join([p.get_text(strip=True) for p in paragraphs])
    return content

def sov_uzdaily():
    url = "https://www.uzdaily.uz/en/section/1/"

    headers = {
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        articles = []
        content_blocks = soup.find_all("a", class_="item_news_block")
        
        for block in content_blocks:
            link = block.get("href")
            if link:
                full_link = f"https://www.uzdaily.uz{link}"
            else:
                full_link = None
            date_span = block.find("span", class_="date")
            date = date_span.get_text(strip=True) if date_span else None

            if date:
                # Parse the date assuming the input format is 'dd/mm/yyyy'
                parsed_date = datetime.strptime(date, '%d/%m/%Y')
                formatted_date = parsed_date.strftime('%Y-%m-%d')
            else:
                formatted_date = None

            title_span = block.find("span", class_="name")
            title = title_span.get_text(strip=True) if title_span else None
            content = get_content_uz(full_link)
            matched_keywords = is_ca_related(title, content, sovereign_keywords)
            if not matched_keywords:
                logging.debug(f"Skipping non-relevant article: {title}")
                continue
            articles_info = ({
                "title": title,
                "date": formatted_date,
                "link": full_link,
                "content": content,
                "source": "UzDaily",
                "sector": "sovereigns",
                "region": "CentralAsia",
                "keywords": matched_keywords

            })
            save_article(articles_info)
            articles.append(articles_info)
    return articles
        
