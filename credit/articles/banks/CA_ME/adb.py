import json
import requests
import cloudscraper
from bs4 import BeautifulSoup
from langdetect import detect, DetectorFactory
from dateutil import parser
from utils.check import filter_articles_by_region_2
from utils.keywords import COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS
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

def both_adb_articles():
    url = "https://www.adb.org/news/releases"
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        articles = []

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            article_list = soup.find('div', class_='views-list').find_all('li')

            for item in article_list:
                try:
                    # Extract date from non-empty meta span
                    date_spans = item.find_all('span', class_='meta')
                    date_text = ""
                    for span in date_spans:
                        if span.text.strip():
                            date_text = span.text.strip()
                            break
                    
                    if not date_text:
                        continue

                    # Extract title and link from anchor tag
                    title_tag = None
                    anchors = item.find_all('a')
                    for a in anchors:
                        href = a.get('href')
                        if href and '/news/' in href:
                            title_tag = a
                            break
                    
                    if not title_tag:
                        continue

                    title = title_tag.text.strip()
                    link = "https://www.adb.org" + title_tag['href']
                    formatted_date = parser.parse(date_text).strftime("%Y-%m-%d")
                    content = adb_article_content(link)
                    if title and link and content:
                        detected_lang = detect(title)
                        if detected_lang != "en":
                            title = translate_text(title, detected_lang)
                        detected_lang = detect(content)
                        if detected_lang != "en":
                            content = translate_text(content, detected_lang)
                        region, keywords = filter_articles_by_region_2(
                            title, content, COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS
                        )
                        if keywords:
                            articles_info = ({
                                'date': formatted_date,
                                'title': title,
                                'link': link,
                                'content': content,
                                'region': region,
                                'keywords': keywords,
                                'sector': 'banks',
                                'source': 'ADB'
                            })
                            save_article(articles_info)
                            articles.append(articles_info)

                except Exception as e:
                    print(f"Error processing article: {e}")
            return articles
    except Exception as e:
        print(f"ADB Banks Error: {e}")
        return []
