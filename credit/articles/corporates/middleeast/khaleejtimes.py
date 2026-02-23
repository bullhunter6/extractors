import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.check import me_related
from utils.db import save_article

keywords =[
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
    "Tecom Group", "Union Properties", "banking",
]

def khaleejtimes_articles():
    url = "https://www.khaleejtimes.com/business/banking-and-finance"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    articles=[]
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles_div = soup.find_all('article', class_=['listing-normal-teasers', 'listing-top-main-teaser'])

        for article in articles_div:
            title_tag = article.find('h2') or article.find('h3')
            link_tag = title_tag.find('a') if title_tag else None
            title = title_tag.text.strip() if title_tag else "No Title" 
            link = link_tag['href'] if link_tag else "No Link"

            if link and not link.startswith("http"):
                link = "https://www.khaleejtimes.com" + link

            try:
                content_response = requests.request("GET", link, headers=headers, timeout=30)
            except Exception as e:
                print(f"Error fetching article {link}: {e}")
                continue

            if content_response.status_code == 200:
                content_soup = BeautifulSoup(content_response.text, 'html.parser')
                content_div = content_soup.find('div', class_ = 'col-12 col-lg-9 col-md-9 details article-center-wrap-nf')
                content = ""
                if content_div:
                    content = content_div.get_text(strip=True)

                date_div = content_soup.find('div', class_='timestamp-latnw-nf')
                formatted_date = datetime.now().strftime("%Y-%m-%d")
                if date_div:
                    date_text = date_div.text.strip()
                    published_date_line = date_text.split('\n')[0]
                    import re
                    match = re.search(r"(\d{1,2}\s+\w{3}\s+\d{4})", published_date_line)
                    if match:
                        date = match.group(1)
                        formatted_date = datetime.strptime(date, "%d %b %Y").strftime("%Y-%m-%d")


                    matched_keywords = me_related(title, content, keywords)
                    if not matched_keywords:
                        continue
                    artricle_data = ({
                        "title": title,
                        "link": link,
                        "date": formatted_date,
                        "content": content,
                        "keywords": matched_keywords,
                        "source": "Khaleej Times",
                        "region": "MiddleEast",
                        "sector": "corporates",
                    })
                    save_article(artricle_data)
                    articles.append(artricle_data)
    return articles





