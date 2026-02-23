import requests
from bs4 import BeautifulSoup
import json
from dateutil.parser import parse
from utils.check import is_ca_related
from utils.keywords import CA_KEYWORDS
from utils.db import save_article
import logging

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


def extract_article_content(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "nur_user_id=9b8b628d-ba3f-45e4-9c3c-4ca8f20cceb7; device_id=ded0f0f8-63f6-40ec-aa8a-f97c5b199ee7;",
        "priority": "u=0, i",
        "referer": "https://www.nur.kz/nurfin/banks/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
    except Exception as e:
        print(f"Error fetching content for {url}: {e}")
        return ""

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        content_block = soup.find("div", class_="formatted-body__content--wrapper")
        paragraphs = content_block.find_all("p") if content_block else []
        content = "\n".join([p.get_text(strip=True) for p in paragraphs])

        return content
    return ""

def nurkz_bk():
    url = "https://www.nur.kz/nurfin/banks/"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "nur_user_id=9b8b628d-ba3f-45e4-9c3c-4ca8f20cceb7",
        "priority": "u=0, i",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
    except Exception as e:
        print(f"Error fetching main page {url}: {e}")
        return []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []
        article_blocks = soup.find_all("article", class_="article-card")

        for block in article_blocks:
            title_tag = block.find("a", class_="article-card__title")
            ru_title = title_tag.get_text(strip=True) if title_tag else None
            link = title_tag["href"] if title_tag else None
            
            if link and not link.startswith("http"):
                link = "https://www.nur.kz" + link
                
            date_tag = block.find("time", class_="article-card__date")
            date = date_tag["datetime"] if date_tag else None
            ru_content = extract_article_content(link)

            #translate title and content
            title = translate_text(ru_title)
            content = translate_text(ru_content)
            formatted_date = parse(date).strftime("%Y-%m-%d")
            matched_keywords = is_ca_related(title, content, CA_KEYWORDS)
            if not matched_keywords:
                logging.debug(f"Skipping non-relevant article: {title}")
                continue

            articles_info = ({
                "title": title,
                "link": link,
                "date": formatted_date,
                "content": content,
                "source": "Nur.kz",
                "keywords": matched_keywords,
                "region": "CentralAsia",
                "sector": "banks"
            })
            articles.append(articles_info)
            save_article(articles_info)

        return articles