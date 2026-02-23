import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from utils.check import me_related
from utils.db import save_article

cp_GULF_KEYWORDS = [
    "Fitch Ratings","Moody's", "credit rating", "credit rating agency", "rating methodology","credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", 
    "credit rating scale", "investment grade", "speculative grade", "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", 
    "rating downgrade", "rating watch", "credit rating review", "bond issuance","sovereign bonds", "M&A", "credit risk", "assigns", "withdraws", "affirms", "upgrades", "downgrades", 
    "guarantee", "guaranty", "guaranteed", "secured", "unsecured",

    "corporate issuance","corporate issuances","IPO","corporate rating", "corporate bonds", "standalone credit profile", "issuer default rating", "recovery rating", "recovery percentage", "government related entity", 
    "corporate family rating", "debt capital market", "corporate sukuk", "Sukuk issuance", "bond issuance", "green bonds", "sukuk", "sukuk issuance", "sukuk market",
    
    "Abu Dhabi National Energy Company", "TAQA", "National Central Cooling", 
    "Vista Global Holding", "ABU DHABI FUTURE ENERGY COMPANY", "Masdar", "DP WORLD", "Shelf Drilling Holdings", 
    "Fertiglobe", "Abu Dhabi Ports Company", "AD Ports Group", "Senaat", "EQUATE Sukuk", "Kuwait Projects", 
    "Damac", "Emaar", "Emirates Telecommunications Group Company", "Etisalat", "Aldar", "ADNOC", "Mamoura", 
    "Abu Dhabi Developmental Holding Company", "DUBAI AEROSPACE ENTERPRISE", "Majid Al Futtaim", "ACWA", 
    "EMIRATES SEMB CORP WATER AND POWER COMPANY", "EWEC", "Oztel", "RUWAIS", "SWEIHAN", "Abu Dhabi Crude Oil Pipeline", 
    "ADCOP", "Dae Funding", "Five Holdings", "Dubai Electricity and Water Authority", "DEWA", "Arada Developments", 
    "Ittihad International Investment", "DIFC Investments", "Emirates Strategic Investment Company", 
    "Private Department", "Taghleef Industries Holdco", "Taghleef Industries Topco", "Vantage Drilling International", 
    "Emirates Airline", "Telford Offshore", "Aerotranscargo FZE", "Brooge Petroleum and Gas Investment Company FZC", 
    "Telford Finco", "ACWA Power Capital Management", "2Rivers DMCC", "Eros Media World", "MRV Holding", 
    "Habtoor International", "A D N H Catering", "Abu Dhabi Aviation", "Abu Dhabi National for Building Materials", 
    "Abu Dhabi National Hotels", "Abu Dhabi National Oil Company For Distribution", "Abu Dhabi Ship Building", 
    "ADNOC Drilling Company", "ADNOC Gas", "ADNOC Logistics & Services", "Agility Global", "Agthia Group", 
    "Air Arabia", "AL KHALEEJ Investment", "Al Seer Marine Supplies & Equipment Company", "Alef Education Holding", 
    "Alpha Dhabi Holding", "Americana Restaurants International", "APEX INVESTMENT", "Aram Group", "Aramex", 
    "Borouge", "BURJEEL HOLDINGS", "Dana Gas", "Depa", "Deyaar Development", "Drake & Scull International", 
    "Dubai Investments", "Dubai Taxi Company", "E7 Group", "Easy Lease Motorcycle Rental", "Emaar Development", 
    "Emirates Central Cooling Systems Corporation", "Emirates Driving Company", "Emirates Integrated Telecommunications Company", 
    "Emirates Reem Investments", "EMSTEEL BUILDING MATERIALS", "ESG EMIRATES STALLIONS GROUP", "ESHRAQ INVESTMENTS", 
    "FOODCO NATIONAL FOODSTUFF", "Fujairah Building Industries", "Fujairah Cement Industries", "Ghitha Holding", 
    "Gulf Cement Co", "Gulf Medical Projects Company", "Gulf Navigation Holding", "Gulf Pharmaceutical Industries", 
    "HILY HOLDING", "International Holding Company", "Manazel", "MBME GROUP", "Modon Holding", "National Cement Co", 
    "National Corporation for Tourism & Hotels", "NATIONAL MARINE DREDGING COMPANY", "NMDC Energy", "Orascom Construction", 
    "PALMS SPORTS", "Parkin Company", "PHOENIX GROUP", "Presight AI Holding", "Pure Health Holding", "RAK Ceramics", 
    "RAK Properties", "Ras Al Khaimah Co for White Cement & Construction Materials", "Salik Company", 
    "Sharjah Cement and Industrial Development Company", "SPACE42", "Spinneys 1961 Holding", "Taaleem Holdings", 
    "Tecom Group", "Union Properties"
]


def gulfnews_cp():
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
        matched_keywords = me_related(title, description, cp_GULF_KEYWORDS)
        if not matched_keywords:
            logging.debug(f"Skipping non-relevant article: {title}")
            continue
        articles_data = {
            "title": title,
            "date": updated_date,
            "link": link,
            "content": description,
            "source": "Gulf News",
            "region": "MiddleEast",
            "sector": "corporates",
            "keywords": matched_keywords
        }
        save_article(articles_data)
        articles.append(articles_data)
    
    return articles