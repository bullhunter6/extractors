import json
import requests
import time
import logging
import cloudscraper
from bs4 import BeautifulSoup
from langdetect import detect, DetectorFactory
from dateutil import parser
from utils.check import is_ca_related
from utils.keywords import ca_adb_KEYWORDS
from utils.db import save_article

DetectorFactory.seed = 0

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

def get_content_requests(url, session):
    try:
        response = session.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            content_div = soup.find('div', class_='col-lg-8 offset-lg-1 col-md-10 offset-md-1')
            if content_div:
                paragraphs = content_div.find_all('p')
                article_content = []
                for paragraph in paragraphs:
                    text = paragraph.get_text(strip=True)
                    if text:
                        article_content.append(text)
                return "\n".join(article_content)
    except Exception as e:
        print(f"DEBUG: Error fetching content for {url}: {e}")
    return ""

def adb_articles():
    url = "https://www.adb.org/search0/country/kazakhstan/country/kyrgyz-republic/country/tajikistan/country/uzbekistan/language/en/type/article/type/blog/type/infographic/type/news/type/oped/type/photo_essay/type/speech/type/video"
    
    print("DEBUG: Fetching ADB data with cloudscraper...")
    
    scraper = cloudscraper.create_scraper()
    
    try:
        response = scraper.get(url)
        if response.status_code != 200:
            print(f"DEBUG: Failed to fetch list page. Status: {response.status_code}")
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        list_div = soup.find('div', class_='views-list')
        if not list_div:
            print("DEBUG: Could not find article list div.")
            return []
            
        article_list = list_div.find_all('li')
        print(f"DEBUG: Found {len(article_list)} items in list.")
        
        articles = []
        for item in article_list:
            try:
                date_span = item.find('span', class_='meta')
                if not date_span: continue
                
                date_text = date_span.text.strip().split('|')[0].strip()
                title_tag = item.find('h3').find('a')
                if not title_tag: continue
                
                title = title_tag.text.strip()
                link = "https://www.adb.org" + title_tag['href']
                
                try:
                    formatted_date = parser.parse(date_text).strftime('%Y-%m-%d')
                except:
                    formatted_date = date_text
                
                content = get_content_requests(link, scraper)
                
                if title and link and content:
                    # Translation logic
                    try:
                        detected_lang = detect(title)
                        if detected_lang != "en":
                            title = translate_text(title, detected_lang)
                        
                        if len(content) > 50:
                            detected_lang_content = detect(content)
                            if detected_lang_content != "en":
                                content = translate_text(content, detected_lang_content)
                    except Exception as e:
                        print(f"DEBUG: Translation error: {e}")

                    matched_keywords = is_ca_related(title, content, ca_adb_KEYWORDS)
                    if not matched_keywords:
                        # print(f"DEBUG: Skipped (no keywords): {title}")
                        continue

                    articles_info = ({
                                    'date': formatted_date,
                                    'title': title,
                                    'link': link,
                                    'content': content,
                                    'region': "CentralAsia",
                                    'keywords': matched_keywords,
                                    'sector': 'banks',
                                    'source': 'ADB'
                                })
                    save_article(articles_info)
                    articles.append(articles_info)
                    print(f"DEBUG: Saved article: {title}")
                    
            except Exception as e:
                print(f"DEBUG: Error processing item: {e}")
                continue
                
        return articles

    except Exception as e:
        print(f"DEBUG: Error in adb_articles with cloudscraper: {e}")
        return []

