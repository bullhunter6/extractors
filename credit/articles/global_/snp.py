import json
import requests
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils.db import save_article
import re
import os

KEYWORDS = ["outlook", "credit rating", "rating action", "sovereign", "default", "upgrade", "downgrade"]

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

def me_related(title, keywords):
    content = title.lower()
    keyword_mapping = {keyword.lower(): keyword for keyword in keywords}
    pattern = r'\b(?:' + '|'.join(re.escape(keyword.lower()) for keyword in keywords) + r')\b'
    matched_keywords_lower = re.findall(pattern, content)
    matched_keywords_original = sorted({keyword_mapping[kw] for kw in matched_keywords_lower})

    return matched_keywords_original

def snp_global():
    # Suppress verbose logging from Selenium and urllib3
    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('WDM').setLevel(logging.WARNING)

    url = "https://www.spglobal.com/api/apps/spglobal-prod/query/spglobal-prod?q=*%3A*&rows=300&pagenum=1&sort=es_unified_dt%20desc&fq=es_content_type_s:(%22Annual%20Report%22OR%22Articles%22OR%22Blog%22OR%22Editorial%22OR%22Expert%20Bio%22OR%22Market%20Intelligence%20Research%22OR%22News%22OR%22PDF%20Details%22OR%22Podcast%22OR%22Press%20Releases%22OR%22Products%22OR%22Special%20Reports%22OR%22Subscriber%20Notes%22OR%22Video%22)&division=corporate"

    print("DEBUG: Starting Selenium to fetch S&P Global data...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
    
    try:
        wdm_path = ChromeDriverManager().install()
        if os.path.isdir(wdm_path):
             executable_path = os.path.join(wdm_path, "chromedriver.exe")
        else:
             executable_path = wdm_path
             
        if not executable_path.endswith(".exe"):
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
        
        # Wait for a bit to ensure page loads
        time.sleep(5)
        
        # Selenium wraps the JSON in HTML, so we need to extract the text content
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
            
            if "error" in data:
                print(f"DEBUG: API returned error: {data.get('msg', 'Unknown error')}")
                return []

            elements = data.get('response', {})
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
                
                if link.startswith("http"):
                    full_link = link
                elif link.startswith("/"):
                    full_link = f"https://www.spglobal.com{link}"
                else:
                    full_link = f"https://www.spglobal.com{link}" if link else "N/A"

                if isinstance(content, list):
                    content = ' '.join(content)
                
                if content:
                    keywords = me_related(title, KEYWORDS)
                    if keywords:
                        if "Daily Update" in title:
                            continue
                        articles_info = ({
                            "title": title,
                            "date": date,
                            "link": full_link,
                            "content": content,
                            "region": "global",
                            "keywords": keywords,
                            "source": "S&P Global",
                            "sector": "global"
                        })
                        save_article(articles_info)
                        articles.append(articles_info)
        except json.JSONDecodeError:
            print("DEBUG: Failed to parse JSON response from Selenium.")
            # print(f"DEBUG: Content preview: {json_text[:200]}")
            
        return articles

    except Exception as e:
        print(f"DEBUG: Error in snp_global with Selenium: {e}")
        try:
            driver.quit()
        except:
            pass
        return []

    return articles