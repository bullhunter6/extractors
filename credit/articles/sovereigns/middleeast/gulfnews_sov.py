import requests
from datetime import datetime
import logging
from utils.check import me_related
from utils.db import save_article

gf_sovereign_keywords =[#removed all countries names and Dubai and Adu Dhabi
    "sovereign rating",
    
    "Finance system","local goverment","goverment","goverment bonds","goverment spending","goverment budget",
    "goverment deficit","goverment surplus","goverment revenue","goverment expenditure","goverment fiscal policy","goverment monetary policy","goverment stimulus","goverment recovery",
    "goverment growth","goverment outlook","goverment impact","goverment contraction","goverment indicators","goverment rate cut",
    "goverment interest rate","goverment interest rates","goverment central bank","goverment central banks","goverment monetary policy","goverment fiscal policy",
    "goverment budget","goverment budgets","goverment deficit","goverment deficits","goverment government debt","goverment debt to GDP","goverment GDP","goverment GDP growth",
    "goverment economy","goverment economic","goverment economic growth","goverment economic outlook","goverment economic recovery","goverment economic stimulus",
    "goverment economic stimulus package","goverment economic impact","goverment economic contraction","goverment economic indicators","goverment rate cut",
    "goverment mortgage","goverment mortgages",'monetary policy','fiscal policy','goverment budget','goverment budgets','government debt','debt to GDP',
    'GDP growth','GDP growth',"GDP Decline", "GDP Trends", "National GDP", "GDP Analysis","GDP Forecast", "GDP Projections", "Comparative GDP Analysis", "GDP per Capita",
    "economic growth","economic outlook","economic recovery","economic stimulus","private sector","public sector","sovereign wealth fund","sovereign wealth funds",
    "economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgages","sukuk","economic growth","economic outlook",
    "economic recovery","economic stimulus","economic stimulus package","economic impact","economic contraction","economic indicators","rate cut",
    
]


def gulfnews_sov():
    url = "https://gulfnews.com/api/v1/collections/business-component4?&item-type=story&offset=0&limit=20"

    payload = {}
    headers = {
        'sec-ch-ua-platform': '"Windows"',
        'Referer': 'https://gulfnews.com/business/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'Cookie': 'visid_incap_1101165=KI64tySQQr+wQXXM0IIeLza7RmcAAAAAQUIPAAAAAAAVUWhq3UM6ZlE5vDA6BeCD'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    items = response.json().get('items', [])
    articles = []

    for item in items:
        title = item['story'].get('headline', ['No headline found'])
        slug = item['story'].get('slug', ['No slug found'])
        link = f"https://gulfnews.com/business/{slug}"
        story = item.get('story', {})
        updated_at = story.get('updated-at')
        description_parts = []
        cards = story.get('cards', [])
        for card in cards:
            elements = card.get('story-elements', [])
            for element in elements:
                if element.get('type') == 'text':
                    description_parts.append(element.get('text', '').strip())
        description = ' '.join(description_parts).strip()
        if updated_at:
            updated_date = datetime.fromtimestamp(int(updated_at) / 1000).strftime('%Y-%m-%d')
        else:
            updated_date = "No date found"
        matched_keywords = me_related(title, description, gf_sovereign_keywords)
        if not matched_keywords:
            logging.debug(f"Skipping non-relevant article: {title}")
            continue
        
        if 'india' in title.lower():
            continue

        articles_data = {
            "title": title,
            "date": updated_date,
            "link": link,
            "content": description,
            "source": "Gulf News",
            "region": "MiddleEast",
            "sector": "sovereigns",
            "keywords": matched_keywords
        }
        save_article(articles_data)
        articles.append(articles_data)
    
    return articles