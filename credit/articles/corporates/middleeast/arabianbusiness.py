import requests
from bs4 import BeautifulSoup
from utils.check import me_related
from utils.db import save_article
import logging
from dateutil.parser import parse

KEYWORDS = [
    "Fitch Ratings","Moody's", "credit rating", "credit rating agency", "rating methodology","credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", 
    "credit rating scale", "investment grade", "speculative grade", "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", 
    "rating downgrade", "rating watch", "credit rating review", "bond issuance","sovereign bonds", "M&A", "credit risk", "assigns", "withdraws", "affirms", "upgrades", "downgrades", 
    "guarantee", "guaranty", "guaranteed", "secured", "unsecured",

    "corporate issuance","corporate issuances","corporate rating", "corporate bonds", "standalone credit profile", "issuer default rating", "recovery rating", "recovery percentage", "government related entity", 
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

def extract_article_content(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '_pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAEzIBYB2AZgCYArDwBsARmE8AnHy4AOYQAYRskAF8gA; _pcid=%7B%22browserId%22%3A%22m5xlmdlr76us3xfo%22%7D; __pat=14400000; __pvi=eyJpZCI6InYtbTV4bG1kbThwb2l0dGhuZyIsImRvbWFpbiI6Ii5hcmFiaWFuYnVzaW5lc3MuY29tIiwidGltZSI6MTczNjkyNzUzNjE4NH0%3D; __tbc=%7Bkpex%7DBahdtpweRuxMRMfLZg47sYHfEMgUnGoQFWh0xU6wpjx_vNEPw3lYhyVgslM9E3oS; xbc=%7Bkpex%7DPIX15jfDNrNGadaXVVMVXA; datadome=bHlzDDvUFdimOQJaWkcaQz0jPHT6MYPLLl1_SC60hE66ImGKGuIJcvaSdsL4~9TU3RHCOu8iVeVBORXsa1UKRwUjxVEOjtK3DEcbb6G~vFxP_BNnJTshiro~MspbmXih',
        'priority': 'u=0, i',
        'referer': 'https://www.arabianbusiness.com/markets',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='entry-content')
        paragraphs = content_div.find_all('p')
        content = "\n".join(p.get_text(strip=True) for p in paragraphs)

        return content

def arabianbusiness_cp():
    url = "https://www.arabianbusiness.com/markets"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Cookie': 'datadome=bHlzDDvUFdimOQJaWkcaQz0jPHT6MYPLLl1_SC60hE66ImGKGuIJcvaSdsL4~9TU3RHCOu8iVeVBORXsa1UKRwUjxVEOjtK3DEcbb6G~vFxP_BNnJTshiro~MspbmXih'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        article_elements = soup.find_all('article', class_='post-has-excerpt')
        for article in article_elements:
            title_element = article.find('h2', class_='entry-title')
            title = title_element.get_text(strip=True) if title_element else None

            link_element = title_element.find('a') if title_element else None
            link = link_element['href'] if link_element else None

            date_element = article.find('time', class_='entry-date published')
            date = date_element['datetime'] if date_element else None

            content = extract_article_content(link)

            matched_keywords = me_related(title, content, KEYWORDS)
            if not matched_keywords:
                logging.debug(f"Skipping non-relevant article: {title}")
                continue
            articles_info = ({
                'title': title,
                'link': link,
                'date': date,
                'content': content,
                'source': 'Arabian Business',
                'keywords': matched_keywords,
                'region': 'MiddleEast',
                'sector': 'corporates'
            })
            save_article(articles_info)
            articles.append(articles_info)

        return articles