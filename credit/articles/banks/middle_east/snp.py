import json
import requests
from langdetect import detect
from utils.db import save_article
from utils.check import me_related
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

KEYWORDS = [#removed first part, 
    "bond issuance", "sovereign bonds", "M&A","financial institutions", "financial institution", "bank bonds", "global banks","development bank", "development banks","sukuk",
    "return on equity", "ROE", "ROA", "retun on assets","equity","UAE bank","UAE banks", "banking system", "Finance system", "Basel", "banking regulations","NPLs","Non-Performing", 
    "Non Performing", "NPAs", "credit risk", "reinsurance", "global banking", "insurance", "banking regulations","open banking", "financial centre","anti-money laundering","banks' assets",
    "tax","financial market","financial markets","financial stability","financial sector","financial services","financial system","financial technology","fintech","financial inclusion","banking sector",
    "private sector","public sector",
    
    "banking",

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


def translate_text(text, source_lang, target_lang="en"):
    url = "https://translate-pa.googleapis.com/v1/translateHtml"
    headers = {
        'accept': '*/*',
        'content-type': 'application/json+protobuf',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-goog-api-key': 'AIzaSyATBXajvzQLTDHEQbcpq0Ihe0vWDHmO520'
    }
    payload = json.dumps([
        [text, source_lang, target_lang],
        "te_lib"
    ])

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        try:
            return response.json()[0][0]
        except (IndexError, KeyError):
            print("Error parsing translation response.")
            return text
    else:
        print(f"Translation failed with status code {response.status_code}")
        return text

def fetch_api_data_with_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        # First visit the search page to get cookies/token
        driver.get("https://www.spglobal.com/en/search")
        time.sleep(5)
        
        token_cookie = driver.get_cookie('search-token')
        if not token_cookie:
            logging.error("No search-token cookie found")
            driver.quit()
            return None
            
        token = token_cookie['value']
        
        script = f"""
        return fetch("{url}", {{
            headers: {{
                "authorization": "Bearer {token}",
                "accept": "application/json, text/plain, */*"
            }}
        }}).then(response => response.json());
        """
        
        data = driver.execute_script(script)
        driver.quit()
        return data
    except Exception as e:
        logging.error(f"Error fetching API data with Selenium: {e}")
        return None

def snp_me():
    url = "https://www.spglobal.com/api/apps/spglobal-prod/query/spglobal-prod?q=*%3A*&rows=50&pagenum=1&sort=es_unified_dt%20desc&fq=es_content_type_s:(%22Blog%22OR%22Corrections%22OR%22Articles%22OR%22Expert%20Bio%22OR%22Indices%20Research%22OR%22Market%20Intelligence%20Research%22OR%22News%22OR%22PDF%20Details%22OR%22Podcast%22OR%22Press%20Releases%22OR%22Products%22OR%22Subscriber%20Notes%22OR%22Symbols%22OR%22Video%22)&fq=es_location_ss:(%22Middle%20East%22)&division=corporate"

    data = fetch_api_data_with_selenium(url)
    articles = []
    if data:
        elements = data.get('response', [])
        docs = elements.get('docs', [])
        for doc in docs:
            title = doc.get('es_title_t', '')
            content = doc.get('es_body_content_txt', [])
            date = doc.get('es_unified_dt', '')
            link = doc.get('es_url_s', '')
            full_link = f"https://www.spglobal.com{link}"
            if link.startswith("http"):
                full_link = link
            elif link.startswith("/"):
                full_link = f"https://www.spglobal.com{link}"
            else:
                full_link = "N/A"

            if isinstance(content, list):
                content = ' '.join(content)
            if content:
                try:
                    detected_lang_title = detect(title)
                except:
                    detected_lang_title = "en"
                if detected_lang_title != "en":
                    title = translate_text(title, detected_lang_title)
                
                try:
                    detected_lang_content = detect(content)
                except:
                    detected_lang_content = "en"
                if detected_lang_content != "en":
                    content = translate_text(content, detected_lang_content)
                
                matched_keywords = me_related(title, content, KEYWORDS)
                if not matched_keywords:
                    logging.debug(f"Skipping non-relevant article: {title}")
                    continue
                
                articles_info = ({
                        "title": title,
                        "date": date,
                        "link": full_link,
                        "content": content,
                        "region": 'MiddleEast',
                        "keywords": matched_keywords,
                        "source": "S&P Global",
                        "sector": "banks"
                    })
                save_article(articles_info)
                articles.append(articles_info)

    return articles