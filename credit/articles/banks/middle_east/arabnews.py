from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import re
from bs4 import BeautifulSoup
from utils.check import me_related
from utils.db import save_article
import logging
from dateutil.parser import parse
from datetime import datetime

KEYWORDS = [
    "Fitch Ratings", "S&P Global", "Moody's", "credit rating", "credit rating agency", "rating methodology", "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "Credit rating scale", "investment grade", "speculative grade",
    "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review",
    
    "bond issuance", "sovereign bonds", "M&A","financial institutions", "financial institution", "bank bonds", "global banks","development bank", "development banks","sukuk",
    "return on equity", "ROE", "ROA", "retun on assets","equity","UAE bank","UAE banks", "banking system", "Finance system", "Basel", "banking regulations","NPLs","Non-Performing", 
    "Non Performing", "NPAs", "credit risk", "reinsurance", "global banking", "insurance sector", "banking regulations","open banking", "financial centre","anti-money laundering","banks' assets",
    "financial market","financial markets","financial stability","financial sector","financial services","financial system","financial technology","fintech","financial inclusion","banking sector",

    "First Abu Dhabi Bank", "FAB", "Emirates NBD", "Central Bank of the UAE", "CBUAE", "Abu Dhabi Commercial Bank", "ADCB", "Dubai Islamic Bank", "DIB", "Mashreq Bank", "Mashreq", "Mashreqbank", "Abu Dhabi Islamic Bank", "ADIB", "HSBC Bank Middle East", "HSBC UAE",
    "Commercial Bank of Dubai", "CBD", "Emirates Islamic", "RAK Bank", "The National Bank of Ras Al Khaimah", "Sharjah Islamic Bank", "SIB", "National Bank of Fujairah", "NBF", "Citibank UAE", "Bank of Sharjah",
    "Ajman Bank", "Arab Bank for Investment and Foreign Trade", "Al Masraf", "Arab Bank UAE", "Commercial Bank International", "CBI", "United Arab Bank", "UAB", "Emirates Development Bank", "EDB", "National Bank of Umm Al Qaiwain",
    "NBQ", "Al Hilal Bank", "Wio Bank", "Invest Bank", "Arab Monetary Fund", "AMF", "Emirates Investment Bank", "Tamweel", "Finance House", "Arab Trade Financing Program", "Mashreq Al Islami", "Credit Europe Bank Dubai",
    "Orient Insurance", "Sukoon Insurance", "Abu Dhabi National Insurance Company", "ADNIC", "Islamic Arab Insurance Company", "SALAMA", "Al Ain Ahlia Insurance", "Emirates Insurance", "Al Wathba National Insurance", "Al Buhaira National Insurance",
    "Union Insurance", "National General Insurance", "NGI", "Al Dhafra Insurance", "Abu Dhabi National Takaful Company", "Dubai Islamic Insurance and Reinsurance Company", "AMAN", "Dubai National Insurance and Reinsurance", "DNIR",
    "Al-Sagr National Insurance", "Methaq Takaful Insurance", "RAK Insurance", "Dubai Insurance", "Saudi Central Bank", "SAMA", "Saudi National Bank", "SNB", "Al Rajhi Bank", "Riyad Bank", "Saudi Awwal Bank", "SAB", "Banque Saudi Fransi",
    "BSF", "Alinma Bank", "Arab National Bank", "ANB", "Bank Albilad", "Saudi Investment Bank", "SAIB", "Bank AlJazira", "BAJ", "Gulf International Bank", "GIB Saudi", "Islamic Development Bank", "IDB", "Arab Petroleum Investments Corporation",
    "APICORP", "Islamic Corporation for the Development of the Private Sector", "ICD", "Tamweel Aloula", "Al-Yusr Leasing and Financing", "Nayifat Finance", "The Arab Investment Company", "TAIC", "AJIL Financial Services",
    "International Islamic Trade Finance Corporation", "ITFC", "Morabaha Marina Financing", "Alraedah Finance", "Aljabr Finance", "Quara Finance", "Al-Amthal Finance", "Gulf Finance Company", "The Company for Insurance", "Bupa Arabia",
    "Al Rajhi Insurance", "Al Rajhi Cooperative Insurance", "Walaa Cooperative Insurance", "Walaa Insurance", "Arabian Shield Insurance", "MedGulf Cooperative", "MedGulf Insurance", "Gulf Insurance Group", "Saudi Re",
    "Allianz Saudi Fransi Insurance", "Saudi Cooperative Insurance", "Al-Etihad Cooperative", "Al-Etihad Insurance", "Arabia Insurance Cooperative", "Malath Insurance", "United Cooperative Assurance",
    "Islamic Corporation for the Insurance of Investment and Export Credit", "ICIEC", "Buruj Cooperative Insurance", "Chubb Arabia Insurance","AAOIFI","World Bank"
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

def get_content_selenium(driver, url):
    try:
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else "No Title"
        
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
        return "Error", "Error", ""

def arabnews_me():
    url = "https://www.arabnews.com/economy"
    driver = get_driver()
    articles = []
    
    try:
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        items = soup.find_all("div", class_="article-item")
        logging.info(f"Found {len(items)} articles on Arab News Economy page")
        
        for article in items:
            title_tag = article.find("div", class_="article-item-title")
            if not title_tag or not title_tag.find("a"):
                continue
                
            link_tag = title_tag.find("a")
            link = "https://www.arabnews.com" + link_tag["href"]
            
            title, date, content = get_content_selenium(driver, link)
            
            if title == "Error" or not content:
                continue
                
            try:
                # Fix missing space between year and time: "202514:54" -> "2025 14:54"
                date_fixed = re.sub(r'(\d{4})(\d{2}:\d{2})', r'\1 \2', date)
                formatted_date = parse(date_fixed).strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                logging.warning(f"Could not parse date '{date}': {e}")
                formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            matched_keywords = me_related(title, content, KEYWORDS)
            if not matched_keywords:
                logging.info(f"⊘ Skipping non-relevant: {title[:50]}...")
                continue
            
            if 'india' in title.lower() or 'indian' in title.lower():
                continue

            articles_data = {
                "title": title,
                "date": formatted_date,
                "link": link,
                "content": content,
                "source": "Arab News",
                "keywords": matched_keywords,
                "region": "MiddleEast",
                "sector": "banks",
            }
            save_article(articles_data)
            articles.append(articles_data)
            
    except Exception as e:
        logging.error(f"Error in arabnews_me: {e}")
    finally:
        driver.quit()

    return articles


