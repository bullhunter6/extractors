import json
import time
import logging
import re
from datetime import datetime
from bs4 import BeautifulSoup
from dateutil.parser import parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from utils.check import me_related
from utils.db import save_article

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

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def get_content(driver, url):
    try:
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else "Title not found"
        
        date_tag = soup.find('div', class_='entry-date')
        date = date_tag.find('time').get_text(strip=True) if date_tag and date_tag.find('time') else "Date not found"
        
        content_tag = soup.find('div', class_='entry-content')
        content = ""
        if content_tag:
            paragraphs = content_tag.find_all('p')
            content = "\n".join([p.get_text(strip=True) for p in paragraphs])
            
        return title, date, content
    except Exception as e:
        logging.error(f"Error fetching content for {url}: {e}")
        return "Title not found", "Date not found", ""

def arabnews_cp():
    url = "https://www.arabnews.com/economy"
    articles = []
    driver = None
    
    try:
        driver = get_driver()
        driver.get(url)
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        article_items = soup.find_all("div", class_="article-item")
        
        if not article_items:
            logging.warning("No article items found on Arab News economy page.")
            return []

        # Limit to first 15 articles to save time
        for article in article_items[:15]:
            try:
                title_tag = article.find("div", class_="article-item-title")
                if not title_tag:
                    continue
                a_tag = title_tag.find("a")
                if not a_tag:
                    continue
                
                item_title = a_tag.get_text(strip=True)
                link = "https://www.arabnews.com" + a_tag["href"]
                
                # Optimization: Check title first before fetching full content
                matched_keywords = me_related(item_title, "", KEYWORDS)
                if not matched_keywords:
                    logging.debug(f"Skipping non-relevant article by title: {item_title}")
                    continue

                title, date, content = get_content(driver, link)
                
                if date == "Date not found":
                    formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                else:
                    try:
                        # Fix missing space between year and time: "202514:54" -> "2025 14:54"
                        date_fixed = re.sub(r'(\d{4})(\d{2}:\d{2})', r'\1 \2', date)
                        formatted_date = parse(date_fixed).strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Re-check with full content just in case
                matched_keywords = me_related(title, content, KEYWORDS)
                if not matched_keywords:
                    continue

                articles_info = {
                    "title": title,
                    "date": formatted_date,
                    "link": link,
                    "content": content,
                    "source": "Arab News",
                    "keywords": matched_keywords,
                    "region": "MiddleEast",
                    "sector": "corporates",
                }
                save_article(articles_info)
                articles.append(articles_info)
            except Exception as e:
                logging.error(f"Error processing article item: {e}")
                continue

    except Exception as e:
        logging.error(f"Error in arabnews_cp: {e}")
    finally:
        if driver:
            driver.quit()

    return articles
