import json
import requests
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from langdetect import detect
from utils.check import filter_articles_by_region_2
from utils.db import save_article

COMMON_KEYWORDS = [#removed credit rating, 
    "banking","finance",
    
    "banks", "bank", "financial institutions", "financial institution", "insurance outlook", 'insurance industry', 'insurance conference', 'insurance market', 'insurance sector',"bond issuance",
    "M&A", "bank bonds", "global banks", "global banking", "banking system", "Finance system", "Basel", "banking regulations","banking","NPLs","Non-Performing",
    "Non Performing", "NPAs", "credit risk", "reinsurance","World Bank","Banking Industry Country Risk Assessment",
]
 
MIDDLEEAST_COUNTRY_KEYWORDS = ["UAE", "United Arab Emirates", "Saudi Arabia", "GCC countries", "GCC", "Kuwait", "Oman", "Bahrein", "Qatar", "Dubai", "Abu Dhabi","KSA", "saudi", "Middle east", "RAK","Sharjah", "Ras Al Khamiah","Gulf Cooperation Council",
                               "Persian Gulf", "Islamic Cooperation", "Arab League","Muscat","Red Sea", "Yemen", "Jordan", "MENA", "Organization of the Petroleum Exporting Countries", "Arabic Gulf", "Arabian Sea"]

CENTRALASIA_COUNTRY_KEYWORDS = ["Uzbekistan","Kazakh", "Kazakhstan", "Asia and Pacific", "Central Asia","Azerbaijan","Armenia","Turkmenistan","Kyrgyzstan","Tajikistan","Silk Road","Caspian Sea","Eurasia", "Post-Soviet States","Tashkent","Almaty",
                                "Samarkand","Economic Cooperation Organization","Silk Route","OPEC",]
 
MIDDLEEAST_RARE_KEYWORDS = [
    "sukuk",
                            
    "First Abu Dhabi Bank", "FAB", "Emirates NBD", "Central Bank of the UAE", "CBUAE", "Abu Dhabi Commercial Bank", "ADCB", "Dubai Islamic Bank", "DIB", "Mashreq Bank", "Mashreq", "Mashreqbank", "Abu Dhabi Islamic Bank", "ADIB", "HSBC Bank Middle East", "HSBC UAE",
    "Commercial Bank of Dubai", "CBD", "Emirates Islamic", "RAK Bank", "The National Bank of Ras Al Khaimah", "Sharjah Islamic Bank", "SIB", "National Bank of Fujairah", "NBF", "Citibank UAE", "Bank of Sharjah",
    "Ajman Bank", "Arab Bank for Investment and Foreign Trade", "Al Masraf", "Arab Bank UAE", "Commercial Bank International", "CBI", "United Arab Bank", "Emirates Development Bank", "EDB", "National Bank of Umm Al Qaiwain",
    "NBQ", "Al Hilal Bank", "Wio Bank", "Invest Bank", "Arab Monetary Fund", "AMF", "Emirates Investment Bank", "Tamweel", "Finance House", "Arab Trade Financing Program", "Mashreq Al Islami", "Credit Europe Bank Dubai",
    "Orient Insurance", "Sukoon Insurance", "Abu Dhabi National Insurance Company", "ADNIC", "Islamic Arab Insurance Company", "SALAMA", "Al Ain Ahlia Insurance", "Emirates Insurance", "Al Wathba National Insurance", "Al Buhaira National Insurance",
    "Union Insurance", "National General Insurance", "NGI", "Al Dhafra Insurance", "Abu Dhabi National Takaful Company", "Dubai Islamic Insurance and Reinsurance Company", "AMAN", "Dubai National Insurance and Reinsurance", "DNIR",
    "Al-Sagr National Insurance", "Methaq Takaful Insurance", "RAK Insurance", "Dubai Insurance", "Saudi Central Bank", "SAMA", "Saudi National Bank", "SNB", "Al Rajhi Bank", "Riyad Bank", "Saudi Awwal Bank", "SAB", "Banque Saudi Fransi",
    "BSF", "Alinma Bank", "Arab National Bank", "ANB", "Bank Albilad", "Saudi Investment Bank", "SAIB", "Bank AlJazira", "BAJ", "Gulf International Bank", "GIB Saudi", "Islamic Development Bank", "IDB", "Arab Petroleum Investments Corporation",
    "APICORP", "Islamic Corporation for the Development of the Private Sector", "ICD", "Tamweel Aloula", "Al-Yusr Leasing and Financing", "Nayifat Finance", "The Arab Investment Company", "TAIC", "AJIL Financial Services",
    "International Islamic Trade Finance Corporation", "ITFC", "Morabaha Marina Financing", "Alraedah Finance", "Aljabr Finance", "Quara Finance", "Al-Amthal Finance", "Gulf Finance Company", "The Company for Insurance", "Bupa Arabia",
    "Al Rajhi Insurance", "Al Rajhi Cooperative Insurance", "Walaa Cooperative Insurance", "Walaa Insurance", "Arabian Shield Insurance", "MedGulf Cooperative", "MedGulf Insurance", "Gulf Insurance Group", "Saudi Re",
    "Allianz Saudi Fransi Insurance", "Saudi Cooperative Insurance", "Al-Etihad Cooperative", "Al-Etihad Insurance", "Arabia Insurance Cooperative", "Malath Insurance", "United Cooperative Assurance",
    "Islamic Corporation for the Insurance of Investment and Export Credit", "ICIEC", "Buruj Cooperative Insurance", "Chubb Arabia Insurance","AAOIFI",
    ]

CENTERALASIA_RARE_KEYWORDS = [#removed ADB
    "CIS banks", "National Bank of Foreign Economic Activity", "NBU",
    "Uzpromstroybank", "SQB", "Agrobank", "Asakabank", "Ipoteka Bank", "Kapitalbank", "Xalq Bank",
    "Qishloq Qurilish Bank", "Business Development Bank", "Hamkorbank", "Microcreditbank", "Ipak Yuli",
    "Ipak Yuli Bank", "Aloqabank","Aloqa bank", "Turonbank", "Orient Finans Bank", "Trustbank", "KDB Bank Uzbekistan",
    "KDB Bank", "Asia Alliance Bank", "Invest Finance Bank", "Davr Bank", "Ravnaq Bank", "Uzagroleasing",
    "Universal Bank", "Uzbek Leasing International", "Hi-Tech Bank", "Madad Invest Bank", "Uzagroexport Bank",
    "Ziraat Bank Uzbekistan", "Ziraat Bank", "Alfa Invest Insurance", "Euroasia Insurance", "Impex Insurance",
    "Ingo Uzbekistan Insurance", "Kafil-Sug'urta", "Mosaic", "My Insurance", "Uzbekinvest",
    "National Bank of Kazakhstan", "Halyk Bank", "Baiterek National Managing Holding", "Kaspi.kz", "Kaspi",
    "Kaspi Bank", "Bank CenterCredit", "Development Bank of Kazakhstan", "Otbasy Bank", "ForteBank",
    "First Heartland Jusan Bank", "Eurasian Bank", "Freedom Bank Kazakhstan", "Bereke Bank", "Bank RBK",
    "Agrarian Credit Corporation", "Citibank Kazakhstan", "Altyn Bank (China CITIC)", "Altyn Bank",
    "Home Credit Bank", "KazAgroFinance", "Shinhan Bank Kazakhstan", "Nurbank", "Damu Fund",
    "AB Bank China Kazakhstan", "Qazaq Banki", "Industrial and Commercial Bank of China (Almaty)",
    "KMF Microfinance Organization", "Kazakhstan-Ziraat International Bank", "VTB Bank Kazakhstan",
    "Al Hilal Islamic Bank", "Tengri Bank", "AsiaCredit Bank", "Capital Bank Kazakhstan","Asian Development Bank",
    "Eurasian Development Bank", "KazakhExport Insurance"]

REGIONAL_KEYWORDS = {
    "MiddleEast": MIDDLEEAST_COUNTRY_KEYWORDS,
    "CentralAsia": CENTRALASIA_COUNTRY_KEYWORDS,
}

RARE_KEYWORDS = {
    "MiddleEast": MIDDLEEAST_RARE_KEYWORDS,
    "CentralAsia": CENTERALASIA_RARE_KEYWORDS,
}

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

def snp_bk():
    # Suppress verbose logging from Selenium and urllib3
    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('WDM').setLevel(logging.WARNING)

    url = "https://www.spglobal.com/api/apps/spglobal-prod/query/spglobal-prod?q=*%3A*&rows=300&pagenum=1&sort=es_unified_dt%20desc&fq=es_content_type_s:(%22Articles%22OR%22Blog%22OR%22Corrections%22OR%22Expert%20Bio%22OR%22Indices%20Research%22OR%22Market%20Intelligence%20Research%22OR%22News%22OR%22PDF%20Details%22OR%22Podcast%22OR%22Press%20Releases%22OR%22Products%22OR%22Subscriber%20Notes%22OR%22Symbols%22OR%22Video%22)&division=corporate"

    print("DEBUG: Starting Selenium to fetch S&P Global data...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
    
    try:
        # Explicitly request win64 version if possible, or let WDM handle it but be aware of the issue
        # The error [WinError 193] usually means a 32-bit/64-bit mismatch.
        # We will try to force the path if WDM fails, but WDM should handle it.
        # Let's try a simpler initialization first.
        # service = Service(ChromeDriverManager().install())
        # driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Fallback to direct path if WDM is downloading the wrong architecture or corrupt file
        # Assuming standard installation or WDM path
        import os
        # Try to find the executable in the WDM cache manually
        wdm_path = ChromeDriverManager().install()
        # WDM might return the folder path or the file path depending on version
        if os.path.isdir(wdm_path):
             executable_path = os.path.join(wdm_path, "chromedriver.exe")
        else:
             executable_path = wdm_path
             
        # Fix for the specific error: check if it points to a valid exe
        if not executable_path.endswith(".exe"):
             # Sometimes WDM returns the LICENSE file or similar if not careful
             # Let's try to force a clean install or just use the folder
             folder = os.path.dirname(executable_path)
             executable_path = os.path.join(folder, "chromedriver.exe")

        service = Service(executable_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Step 1: Visit the main page to establish session/cookies
        print("DEBUG: Visiting main S&P page to establish session...")
        driver.get("https://www.spglobal.com/ratings/en/")
        time.sleep(10) # Wait for cookies to be set
        
        # Step 2: Visit the API URL
        print("DEBUG: Visiting API URL...")
        driver.get(url)
        
        # Wait for a bit to ensure page loads (though for JSON API it should be fast)
        time.sleep(5)
        
        page_source = driver.page_source
        
        # Selenium wraps the JSON in HTML, so we need to extract the text content
        # Usually it's inside a <pre> tag or just the body text
        try:
            pre_tag = driver.find_element("tag name", "pre")
            json_text = pre_tag.text
        except:
            # Fallback: try to parse the whole body text
            json_text = driver.find_element("tag name", "body").text

        driver.quit()
        
        articles = []
        try:
            data = json.loads(json_text)
            
            # Check for error response
            if "error" in data:
                print(f"DEBUG: API returned error: {data.get('msg', 'Unknown error')}")
                return []

            elements = data.get('response', {})
            # Ensure elements is a dict before calling .get
            if isinstance(elements, list):
                 print("DEBUG: Unexpected 'response' format (list instead of dict).")
                 return []
                 
            docs = elements.get('docs', [])
            print(f"DEBUG: Found {len(docs)} documents.")
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
                    region, keywords = filter_articles_by_region_2(title, content, COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS)
                    if keywords:
                        if "Daily Update" in title or "Trump" in title:
                            continue
                        articles_info = ({
                            "title": title,
                            "date": date,
                            "link": full_link,
                            "content": content,
                            "region": region,
                            "keywords": keywords,
                            "source": "S&P Global",
                            "sector": "banks"
                        })
                        save_article(articles_info)
                        articles.append(articles_info)
        except json.JSONDecodeError:
            print("DEBUG: Failed to parse JSON response from Selenium.")
            print(f"DEBUG: Content preview: {json_text[:200]}")
            
        return articles

    except Exception as e:
        print(f"DEBUG: Error in snp_bk with Selenium: {e}")
        try:
            driver.quit()
        except:
            pass
        return []

