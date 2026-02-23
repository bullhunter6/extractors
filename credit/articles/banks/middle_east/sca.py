import json
import time
import logging
import requests
import html
from datetime import datetime
from bs4 import BeautifulSoup
from langdetect import detect, DetectorFactory
from utils.check import me_related
from utils.keywords import me_sca_KEYWORDS
from utils.db import save_article

DetectorFactory.seed = 0

ARABIC_MONTHS = {
    'يناير': '01', 'فبراير': '02', 'مارس': '03', 'أبريل': '04',
    'مايو': '05', 'يونيو': '06', 'يوليو': '07', 'أغسطس': '08',
    'سبتمبر': '09', 'أكتوبر': '10', 'نوفمبر': '11', 'ديسمبر': '12'
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

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        if response.status_code == 200:
            try:
                translated = response.json()[0][0]
                return html.unescape(translated)
            except (IndexError, KeyError):
                logging.error("Error parsing translation response.")
                return text
        else:
            logging.error(f"Translation failed with status code {response.status_code}")
            return text
    except Exception as e:
        logging.error(f"Translation request error: {e}")
        return text

def clean_summary(html_summary):
    """
    Clean the HTML content by removing unnecessary tags, styles, and inline attributes.
    """
    if not html_summary:
        return ""
    soup = BeautifulSoup(html_summary, 'html.parser')
    for tag in soup.find_all(True):
        tag.attrs = {}
    text = soup.get_text(separator=' ', strip=True)
    return html.unescape(text)

def parse_arabic_date(date_str):
    """
    Parse Arabic date string like 'الجمعة, 19 ديسمبر 2025' to 'YYYY-MM-DD'.
    """
    try:
        # Remove day name and comma
        clean_date = date_str.split(',')[-1].strip()
        parts = clean_date.split()
        if len(parts) >= 3:
            day = parts[0].zfill(2)
            month_name = parts[1]
            year = parts[2]
            month = ARABIC_MONTHS.get(month_name, '01')
            return f"{year}-{month}-{day}"
    except Exception as e:
        logging.warning(f"Could not parse Arabic date '{date_str}': {e}")
    return datetime.now().strftime('%Y-%m-%d')

def process_article(title, summary, date, link):
    """
    Translate, filter and save article.
    """
    try:
        # Translation logic
        try:
            detected_lang = detect(title)
            if detected_lang != "en":
                title = translate_text(title, detected_lang)
            else:
                title = html.unescape(title)
            
            if summary and len(summary) > 20:
                detected_lang_summary = detect(summary)
                if detected_lang_summary != "en":
                    summary = translate_text(summary, detected_lang_summary)
                else:
                    summary = html.unescape(summary)
        except Exception as e:
            logging.warning(f"Translation error for {title}: {e}")

        matched_keywords = me_related(title, summary, me_sca_KEYWORDS)
        if not matched_keywords:
            logging.debug(f"Skipping non-relevant article: {title}")
            return None

        logging.info(f"Matched keywords for '{title}': {matched_keywords}")
        article_data = {
            'title': title,
            'date': date,
            'content': summary,
            'link': link,
            'source': 'SCA',
            'keywords': ', '.join(matched_keywords),
            'region': 'MiddleEast',
            'sector': 'banks'
        }
        save_article(article_data)
        logging.info(f"Saved article: {title}")
        return article_data
    except Exception as e:
        logging.error(f"Error processing article {title}: {e}")
        return None

def sca_articles():
    """
    Fetch and process articles from SCA website and API.
    """
    results = []
    excluded_ids = []
    session = requests.Session()
    
    # 1. Scrape HTML for latest articles
    html_url = "https://www.sca.gov.ae/ar/media-centre/news"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    logging.info("Fetching SCA HTML page...")
    try:
        response = session.get(html_url, headers=headers, timeout=20)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find articles in the list
            news_items = soup.find_all('div', attrs={'data-attr-news-id': True})
            logging.info(f"Found {len(news_items)} articles in HTML.")
            
            for item in news_items:
                news_id = item['data-attr-news-id']
                excluded_ids.append(news_id)
                
                link_tag = item.find('h3').find('a')
                if not link_tag: continue
                
                title = link_tag.text.strip()
                link = "https://www.sca.gov.ae/" + link_tag['href'].lstrip('/')
                
                date_span = item.find('span', class_='text-aeblack-300')
                date_text = date_span.text.strip() if date_span else ""
                date = parse_arabic_date(date_text)
                
                summary_p = item.find('p')
                summary = summary_p.text.strip() if summary_p else ""
                
                article_data = process_article(title, summary, date, link)
                if article_data:
                    results.append(article_data)
    except Exception as e:
        logging.error(f"Error scraping SCA HTML: {e}")

    # 2. Call API for more articles
    api_url = "https://www.sca.gov.ae/api/PublicApi/GetContentList"
    
    # Get verification token from cookies
    token = session.cookies.get('__RequestVerificationToken')
    
    api_headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': headers['User-Agent'],
        'Referer': html_url,
        'X-Requested-With': 'XMLHttpRequest',
        'RequestVerificationToken': token if token else '',
        'languageCode': 'ar-AE',
        'languageId': '2',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://www.sca.gov.ae'
    }
    
    exclude_str = ",".join(excluded_ids)
    
    filters = [
        {"Key": "LanguageId", "Value": 2, "Operator": "Equal", "OR_AND_Operator": "AND"}
    ]
    
    if excluded_ids:
        filters.append({"Key": "id", "Value": exclude_str, "Operator": "NotIn", "OR_AND_Operator": "AND"})
        
    filters.extend([
        {"Key": "ItemDate1", "Value": "", "Operator": "GreaterEqual", "OR_AND_Operator": "AND"},
        {"Key": "ItemDate1", "Value": "", "Operator": "LessEqual", "OR_AND_Operator": "AND"},
        {"Key": "Status", "Value": "Published", "Operator": "Contains", "OR_AND_Operator": "AND"},
        {"Key": "Status", "Value": "Active", "Operator": "Contains", "OR_AND_Operator": "AND"},
        {"Key": "Status", "Value": "NotArchived", "Operator": "Contains", "OR_AND_Operator": "AND"}
    ])

    payload = {
        "htmlTemplatePath": "ajax-templates/mediahub/newslisting.html",
        "loadResultAsHTML": False,
        "typeId": 2,
        "pageIndex": 1,
        "pageSize": 9,
        "languageId": 2,
        "languageCode": "ar-AE",
        "isArchived": False,
        "imageSize": "full",
        "thumbnailSize": "1d80x1180wFFFFFF",
        "excludeItems": [],
        "FilterGroups": [
            {"OR_AND_Operator": "AND", "Filters": filters}
        ]
    }
    
    logging.info("Fetching SCA API data...")
    try:
        response = session.post(api_url, json=payload, headers=api_headers, timeout=20)
        if response.status_code == 200:
            data = response.json()
            contents = data.get('data', {}).get('contents', [])
            logging.info(f"Found {len(contents)} articles in API.")
            
            for content in contents:
                title = content.get('title', '')
                link = "https://www.sca.gov.ae/" + content.get('link', '').lstrip('/')
                
                # isoItemDate1 format: "2025-11-11 00:11:00"
                iso_date = content.get('isoItemDate1', '')
                date = iso_date.split(' ')[0] if iso_date else datetime.now().strftime('%Y-%m-%d')
                
                summary_html = content.get('fullText', '')
                summary = clean_summary(summary_html)
                if not summary:
                    summary = content.get('introText', '')
                
                article_data = process_article(title, summary, date, link)
                if article_data:
                    results.append(article_data)
        else:
            logging.error(f"SCA API failed with status code {response.status_code}: {response.text}")
    except Exception as e:
        logging.error(f"Error calling SCA API: {e}")
        
    return results
