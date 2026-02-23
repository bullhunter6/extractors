import json
import time
import re
import logging
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dateutil import parser
from bs4 import BeautifulSoup
from utils.check import me_related
from utils.db import save_article

# Suppress selenium and uc logging
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('undetected_chromedriver').setLevel(logging.WARNING)

cp_GULF_KEYWORDS = [
    "corporate rating", "corporate bonds", "debt capital market", "corporate sukuk", "Sukuk issuance", 
    "bond issuance", "green bonds", "Abu Dhabi National Energy Company", "TAQA", "National Central Cooling", 
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
    "Tecom Group", "Union Properties","Latvia","fitch",
]

def get_driver():
    options = uc.ChromeOptions()
    # options.add_argument('--headless') # Headless might be causing issues with Chrome 143
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    # Set a common user agent
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
    
    try:
        driver = uc.Chrome(options=options)
        return driver
    except Exception as e:
        print(f"Failed to initialize undetected-chromedriver: {e}")
        # Fallback to standard selenium if uc fails
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_content(driver, url):
    try:
        driver.get(url)
        time.sleep(5) # Wait for content to load and bypass potential challenges
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = soup.find('div', class_='body-content')
        if not content:
            # Try alternative selectors if Bloomberg changed layout
            content = soup.find('div', class_=re.compile('body-copy|article-body'))
        return content
    except Exception as e:
        print(f"Error fetching content for {url}: {e}")
        return None

def bloomberg():
    api_url = "https://www.bloomberg.com/lineup-next/api/paginate?id=archive_stories&page=phx-fixed-income&offset=0&variation=archive&type=lineup_content"
    
    driver = None
    articles = []
    try:
        driver = get_driver()
        print("Fetching Bloomberg API via Selenium...")
        driver.get(api_url)
        time.sleep(8) # Longer wait for API response
        
        # Extract JSON from page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # UC might show the JSON directly or wrapped in <pre>
        pre = soup.find('pre')
        if pre:
            json_data = pre.text
        else:
            # Sometimes it's just in the body
            body = soup.find('body')
            json_data = body.text if body else ""
            
        try:
            # Clean up potential HTML wrapping if any
            json_data = json_data.strip()
            data = json.loads(json_data)
        except Exception as e:
            print(f"Failed to parse JSON from page: {e}")
            # If it fails, maybe we are blocked or it's not JSON
            if "Forbidden" in page_source or "captcha" in page_source.lower():
                print("Blocked by Bloomberg (403 or Captcha detected)")
            return []

        archives = data.get('archive_stories', {}).get('items', [])
        print(f"Found {len(archives)} items in API.")
        
        for archive in archives:
            title = archive.get('headline', {})
            date_str = archive.get('publishedAt',{})
            if not date_str:
                continue
            
            try:
                date = parser.parse(date_str).strftime("%Y-%m-%d")
            except:
                date = date_str

            url_path = archive.get('url',{})
            link = f"https://www.bloomberg.com{url_path}"
            
            print(f"Fetching content for: {link}")
            content = get_content(driver, link)
            
            content_text = content.text if content else ""
            matched_keywords = me_related(title, content_text, cp_GULF_KEYWORDS)
            
            if not matched_keywords:
                print(f"No keywords matched for: {title}")
                continue
                
            article_data = {
                'title': title,
                'date': date,
                'content': content_text,
                'link': link,
                'source': 'Bloomberg',
                'region': 'MiddleEast',
                'sector': 'corporates',
                'keywords': matched_keywords
            }
            save_article(article_data)
            articles.append(article_data)
            print(f"Saved article: {title}")
            time.sleep(3) # Delay between articles
            
    except Exception as e:
        print(f"General error in bloomberg extractor: {e}")
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
            
    return articles

if __name__ == "__main__":
    results = bloomberg()
    print(f"Total articles fetched: {len(results)}")
    for idx, article in enumerate(results, start=1):
        print(f"Article {idx}: {article['title']} ({article['date']})")



