import json
import requests
import cloudscraper
from bs4 import BeautifulSoup
from langdetect import detect, DetectorFactory
from dateutil import parser
from datetime import datetime
from utils.check import is_ca_related
from utils.db import save_article
import logging

DetectorFactory.seed = 0

sovereign_keywords =[
    "sovereign","sovereign rating","private sector","public sector",
    
    "Asia and Pacific", "Central Asia","Azerbaijan","Armenia","Turkmenistan","Kyrgyzstan","Tajikistan","Kazakhstan","Uzbekistan",
    "Silk Road","Caspian Sea","Eurasia", "Post-Soviet States","Samarkand","Economic Cooperation Organization","Silk Route",
    
    "privatisation","Finance system","local goverment","goverment","goverment bonds","goverment spending","goverment budget",
    "goverment deficit","goverment surplus","goverment revenue","goverment expenditure","goverment fiscal policy","goverment monetary policy","goverment stimulus","goverment recovery",
    "goverment growth","goverment outlook","goverment impact","goverment contraction","goverment indicators","goverment rate cut","goverment mortgage","goverment mortgages",
    "goverment interest rate","goverment interest rates","goverment central bank","goverment central banks","goverment monetary policy","goverment fiscal policy",
    "goverment budget","goverment budgets","goverment deficit","goverment deficits","goverment government debt","goverment debt to GDP","goverment GDP","goverment GDP growth",
    "goverment economy","goverment economic","goverment economic growth","goverment economic outlook","goverment economic recovery","goverment economic stimulus",
    "goverment economic stimulus package","goverment economic impact","goverment economic contraction","goverment economic indicators","goverment rate cut",
    "goverment mortgage","goverment mortgages",'interest rate','interest rates','monetary policy','fiscal policy','goverment budget','goverment budgets','deficit',
    'deficits','government debt','debt to GDP','GDP','GDP growth',"economy","economic growth","economic outlook","economic recovery","economic stimulus",
    "economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgage","mortgages","sukuk","economic growth","economic outlook",
    "economic recovery","economic stimulus","economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgage","mortgages","investments"
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

def adb_article_content(url):
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
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

                full_article = "\n".join(article_content)

                return full_article
    except Exception as e:
        print(f"Error fetching article content: {e}")
        return None

def adb_sov():
    url = "https://www.adb.org/search0/country/kazakhstan/country/kyrgyz-republic/country/tajikistan/country/uzbekistan/language/en/type/article/type/blog/type/event/type/infographic/type/news/type/oped/type/photo_essay/type/speech/type/video"

    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        articles = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            article_list = soup.find('div', class_='views-list').find_all('li')
            for item in article_list:
                try:
                    # Find all meta spans and take the first non-empty one
                    date_tags = item.find_all('span', class_='meta')
                    date = ""
                    for tag in date_tags:
                        if tag.text.strip():
                            date = tag.text.strip().split('|')[0].strip()
                            break
                    
                    # Find the correct link tag (the one with the actual article path)
                    title_tag = None
                    for a in item.find_all('a', href=True):
                        if a['href'].startswith('/news/') or a['href'].startswith('https://www.adb.org/news/'):
                            title_tag = a
                            break
                    
                    if not title_tag:
                        # Fallback to any link with text if no /news/ link found
                        for a in item.find_all('a', href=True):
                            if a.text.strip() and a['href'] and a['href'] != "#":
                                title_tag = a
                                break

                    if not title_tag:
                        continue

                    title = title_tag.text.strip()
                    link = title_tag['href']
                    if not link.startswith('http'):
                        link = "https://www.adb.org" + link

                    try:
                        formatted_date = parser.parse(date, fuzzy=True).strftime("%Y-%m-%d")
                    except Exception:
                        try:
                            formatted_date = parser.parse(title, fuzzy=True).strftime("%Y-%m-%d")
                        except Exception:
                            formatted_date = datetime.now().strftime("%Y-%m-%d")

                    content = adb_article_content(link)
                    if title and link and content:
                        detected_lang = detect(title)
                        if detected_lang != "en":
                            title = translate_text(title, detected_lang)
                        detected_lang = detect(content)
                        if detected_lang != "en":
                            content = translate_text(content, detected_lang)
                    matched_keywords = is_ca_related(title, content, sovereign_keywords)
                    if not matched_keywords:
                        logging.debug(f"Skipping non-relevant article: {title}")
                        continue

                    articles_info = ({
                                    'date': formatted_date,
                                    'title': title,
                                    'link': link,
                                    'content': content,
                                    'region': "CentralAsia",
                                    'keywords': matched_keywords,
                                    'sector': 'sovereigns',
                                    'source': 'ADB'
                                })
                    save_article(articles_info)
                    articles.append(articles_info)
                except Exception as e:
                    print(f"Error processing article: {e}")
        return articles
    except Exception as e:
        print(f"ADB Sovereign Error: {e}")
        return []
