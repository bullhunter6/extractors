import requests
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import datetime
import json
from langdetect import detect, DetectorFactory
from utils.check import is_ca_related
import logging
from utils.db import save_article

CORPORATE_KEYWORDS = [
    "Fitch Ratings","Moody's", "credit rating", "credit rating agency", "rating methodology",
    "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "credit rating scale",
    "investment grade", "speculative grade", "debt rating", "credit rating model", "credit rating criteria",
    "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review", "bond issuance",
    "sovereign bonds", "M&A", "credit risk", "assigns", "withdraws", "affirms", "upgrades", "downgrades", "guarantee", "guaranty", "guaranteed", "secured", "unsecured",

    "privatisation","corporate rating", "corporate bonds", "standalone credit profile", "issuer default rating", 
    "recovery rating", "recovery percentage", "government related entity", "corporate family rating",


    "Uzbek geological exploration", "Uzbek geological", "Chimpharm", "Altynalmas", 
    
    "Navoi Mining and Metallurgical", "Navoi Mining and Metallurgy", "Navoiyuran", 
    "Almalyk Mining and Metallurgical", "Almalyk Mining and Metallurgy", "Almalyk MMC", 
    "Uzbek Metallurgical", "Uzbek Metallurgy", "Uzmetkombinat", "Uzbekneftegaz", "Uztransgaz", 
    "Hududgazta'minot", "Hududgaz", "UzGasTrade", "National Electric Grid of Uzbekistan", 
    "National Electric Grids of Uzbekistan", "Thermal Power Plants", "Regional Electrical Power Networks", 
    "Uzbekgeofizika", "Uzkimyosanoat", "Navoiyazot", "Navoi-Azot", "Navoiazot", 
    "Uzbek Railways", "Oʻzbekiston temir yoʻllari", "O'zbekiston Temir Yollari", 
    "Uzbekiston Temir Yollari", "Ozbekiston Temir Yollari", "Uzbekistan Railways", 
    "Uzbekistan Airways", "Uzbekistan Airports", "Toshshahartransxizmat", "UzAuto", 
    "Uz Auto", "Uzautosanoat", "Uzauto-sanoat", "Uzbektelecom", "Uzbek telecom", 
    "Uztelecom", "O'zbekiston pochtasi", "UzPost", "Uzbekistan Post", "Uzbekcoal", 
    "Artel Electronics", "Dehkanabad Potash Plant", "Dekhkanabad plant of potassium", 
    "Toshkent Metallurgiya Zavodi", "Tashkent Metallurgical Plant", "Tashkent Metallurgy Plant", 
    "SamAuto", "Samarqand Avtomobil zavodi", "SamAvto", "Akfa Aluminium", "Enter Engineering", 
    "Saneg", "Sanoat Energetika Guruhi", "Fargonaazot", "Farg'onaazot", "Hududiy Elektr Tarmoqla", 
    "Uzsungwoo", "QuvasoyCement", "Quvasoy Cement", "Kuvasaycement", "POSCO International Textile", 
    "Promxim Impex", "Kazakhstan Housing Company", "Samruk-Energy", "Samruk-Energo", 
    "Samruk Energy", "Samruk Energo", "Ekibastuz GRES-1", "Ekibastuz GRES 1", 
    "Samruk-Kazyna Construction", "Samruk Kazyna Construction", "Kazpost", "QazPost", 
    "Kazakhtelecom", "Kcell", "Kazakhstan Electricity Grid Operating Company", "KEGOC", 
    "KazMunayGas", "KazTransOil", "Astana Gas", "Astanagas", "Astana-Gas", "QazaqGaz", 
    "Intergas Central Asia", "KazTransGas", "Kazatomprom", "Kazakhstan Temir Zholy", 
    "Qazaqstan Temır Joly", "Kaztemirtrans", "Tengizchevroil", "Eurasian Resources Group", 
    "BI Group", "Kazakhstan Utility Systems", "Mangistau Regional Electricity Network", 
    "Food Contract Corp", "Food Contract Corporation", "TransteleCom", "Kaz Minerals", 
    "Kazakhmys", "BI Development", "Alma Telecommunications", "Batys transit", 
    "KazMunaiGas", "Kaztemirtrans", "Integra Construction"
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
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
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

def adb_all():
    url = "https://www.adb.org/search0/country/kazakhstan/country/kyrgyz-republic/country/tajikistan/country/uzbekistan/language/en/type/article/type/blog/type/event/type/infographic/type/news/type/oped/type/photo_essay/type/speech/type/video"

    payload = {}
    headers = {
    'Cookie': '__cf_bm=7jK0w5r4ZEBtPtofCrBc1qQJ9hfAtYkbw6Ayr1Yv_dw-1734515144-1.0.1.1-AoXVLwA9HIibD0Ul.nsqtEkPi4jz4B0W1zM5z0dpG3uSUsh9CRTiIlnezCcxNv6mra8XlliiD.T1v1xuY.Gx1Q'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
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
                matched_keywords = is_ca_related(title, content, CORPORATE_KEYWORDS)
                if not matched_keywords:
                    logging.debug(f"Skipping non-relevant article: {title}")
                    continue
                article = {
                    'title': title,
                    'date': formatted_date,
                    'link': link,
                    'content': content,
                    'source': 'ADB',
                    'region': "CentralAsia",
                    'sector': 'corporates',
                    'keywords': matched_keywords
                }
                save_article(article)
                articles.append(article)
            except Exception as e:
                print(f"Error processing article: {e}")
    return articles

def adb_cp():
    return adb_all()