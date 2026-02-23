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
    "IPO","sovereign rating","sovereign",
    "Finance system","local goverment","goverment","goverment bonds","goverment spending","goverment budget",
    "goverment deficit","goverment surplus","goverment revenue","goverment expenditure","goverment fiscal policy","goverment monetary policy","goverment stimulus","goverment recovery",
    "goverment growth","goverment outlook","goverment impact","goverment contraction","goverment indicators","goverment rate cut","goverment mortgage","goverment mortgages",
    "goverment interest rate","goverment interest rates","goverment central bank","goverment central banks","goverment monetary policy","goverment fiscal policy",
    "goverment budget","goverment budgets","goverment deficit","goverment deficits","goverment government debt","goverment debt to GDP","goverment GDP","goverment GDP growth",
    "goverment economy","goverment economic","goverment economic growth","goverment economic outlook","goverment economic recovery","goverment economic stimulus",
    "goverment economic stimulus package","goverment economic impact","goverment economic contraction","goverment economic indicators","goverment rate cut",
    "goverment mortgage","goverment mortgages",'interest rate','interest rates','monetary policy','fiscal policy','goverment budget','goverment budgets','deficit',
    'deficits','government debt','debt to GDP',"private sector","public sector","sovereign wealth fund","sovereign wealth funds",
    "economic growth","economic outlook","economic recovery","economic stimulus",'GDP growth',"GDP Decline", "GDP Trends", "National GDP", "GDP Analysis","GDP Forecast", "GDP Projections", "Comparative GDP Analysis", "GDP per Capita",
    "economic stimulus package","economic impact","econoic contraction","economic indicators","rate cut","mortgage","mortgages","sukuk","economic growth","economic outlook",
    "economic recovery","economic stimulus","economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgage","mortgages",
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

import re

def arabnews_sov():
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
                logging.debug(f"Skipping non-relevant article: {title}")
                continue

            articles_info = {
                "title": title,
                "date": formatted_date,
                "link": link,
                "content": content,
                "source": "Arab News",
                "keywords": matched_keywords,
                "region": "MiddleEast",
                "sector": "sovereigns",
            }
            save_article(articles_info)
            articles.append(articles_info)
            
    except Exception as e:
        logging.error(f"Error in arabnews_sov: {e}")
    finally:
        driver.quit()

    return articles
