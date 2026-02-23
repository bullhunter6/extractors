import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import json
from dateutil import parser
from datetime import datetime
from utils.check import is_ca_related
from utils.keywords import CA_KEYWORDS
from utils.db import save_article

def get_session():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def translate_text(text, source_lang="ru", target_lang="en"):
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
        return response.json()[0][0]
    else:
        print(f"Translation failed with status code {response.status_code}")
        return text

def reformat_date(translated_date):
    try:
        date_part = translated_date.split(",")[0].strip()
        if not any(char.isdigit() for char in date_part.split()[-1]):
            date_part += f" {datetime.now().year}"
        if len(translated_date.split(",")) > 1:
            year_part = translated_date.split(",")[1].strip().split(" ")[0]
            if year_part.isdigit():
                date_part += f" {year_part}"
        parsed_date = datetime.strptime(date_part, "%B %d %Y")
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError as e:
        print(f"Error formatting date: {translated_date} - {e}")
        return translated_date

def forbeskz_banks():
    base_url = "https://forbes.kz/"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    
    session = get_session()
    html_content = ""
    try:
        response = session.get(base_url, headers=headers, timeout=30, stream=True)
        if response.status_code != 200:
            print(f"Failed to fetch the page. Status code: {response.status_code}")
            return []
            
        raw_content = b""
        try:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    raw_content += chunk
        except Exception as e:
            print(f"Warning: Incomplete read for {base_url}: {e}")
            
        html_content = raw_content.decode('utf-8', errors='replace')
        
    except Exception as e:
        print(f"Failed to fetch the page {base_url}: {e}")
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    articles = []

    all_news = soup.find_all('div', class_='card mainCard') + soup.find_all('div', class_='card wtImg')
    for card in all_news:
        try:
            link = card.find('a')['href']
            if not link.startswith("http"):
                link = base_url + link

            title = card.find('div', class_='card__title').get_text(strip=True)
            date = card.find('div', class_='card__time').get_text(strip=True)

            try:
                # Also use streaming for article content just in case
                content_response = session.get(link, headers=headers, timeout=30, stream=True)
                content = ""
                if content_response.status_code == 200:
                    article_raw = b""
                    try:
                        for chunk in content_response.iter_content(chunk_size=8192):
                            if chunk:
                                article_raw += chunk
                    except Exception:
                        pass # Ignore incomplete read for article content too
                    
                    content_soup = BeautifulSoup(article_raw.decode('utf-8', errors='replace'), 'html.parser')
                    content_div = content_soup.find('div', class_='content')
                    if content_div:
                        paragraphs = content_div.find_all('p')
                        content = "\n\n".join(p.get_text(strip=True) for p in paragraphs)
            except Exception as e:
                print(f"Error fetching content for {link}: {e}")
                continue

            articles.append({'title': title, 'link': link, 'date': date, 'content': content})
        except Exception as e:
            print(f"Error processing card: {e}")
            continue

    filtered_articles = []
    for article in articles:
        article['title'] = translate_text(article['title'])
        translated_date = translate_text(article['date'])
        formatted_date = parser.parse(translated_date).strftime('%Y-%m-%d')
        article['date'] = formatted_date
        article['content'] = translate_text(article['content'])

        matched_keywords = is_ca_related(article['title'], article['content'], CA_KEYWORDS)
        if matched_keywords:
            article['keywords'] = matched_keywords
            article['source'] = 'Forbes.kz'
            article['region'] = 'CentralAsia'
            article['sector'] = 'banks'
            save_article(article)
            filtered_articles.append(article)

    return filtered_articles