import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from utils.check import is_ca_related
from utils.keywords import ca_kzkursiv_KEYWORDS
from utils.db import save_article
import json


def kz_kursiv():
    url = "https://kz.kursiv.media/en/"

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'if-modified-since': 'Wed, 27 Nov 2024 07:31:06 GMT',
        'if-none-match': '"34204c95892e4fbdde241ce4e461a3ce"',
        'priority': 'u=0, i',
        'referer': 'https://kz.kursiv.media/en/guide/first-among-equal/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"131.0.6778.86"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.86", "Chromium";v="131.0.6778.86", "Not_A Brand";v="24.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
    except Exception as e:
        print(f"Error fetching main page {url}: {e}")
        return []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        article_cards = soup.select('.post-dynamic-card')
        for card in article_cards:
            title_tag = card.select_one('.post-dynamic-card__title a')
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag['href']

                try:
                    article_response = requests.get(link, headers=headers, timeout=30)
                except Exception as e:
                    print(f"Error fetching article {link}: {e}")
                    continue

                if article_response.status_code == 200:
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')
                    try:
                        
                        publication_date = None
                        date_element = article_soup.select_one('.single-publishing-time__date')
                        if date_element and date_element.has_attr('datetime'):
                            raw_date = date_element['datetime']
                            if raw_date:
                                try:
                                    publication_date = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                                except ValueError:
                                    publication_date = raw_date[:10] if len(raw_date) >= 10 else None
                        
                        if publication_date is None:
                            try:
                                response = requests.get(url, headers=headers, timeout=30)
                                if response.status_code == 200:
                                    soup = BeautifulSoup(response.text, 'html.parser')
                                    script = soup.find('script', type='application/ld+json')
                                    if script:
                                        json_data = json.loads(script.string)
                                        date = json_data.get('datePublished')
                                        if date:
                                            try:
                                                publication_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                                            except ValueError:
                                                publication_date = date[:10] if len(date) >= 10 else None
                            except Exception as e:
                                print(f"Error in fallback date fetch: {e}")

                        tags = [tag.get_text(strip=True) for tag in article_soup.select('.tag-cloud__item')]

                        paragraphs = article_soup.select('.single-body p')
                        content = "\n\n".join(p.get_text(strip=True) for p in paragraphs)

                        matched_keywords = is_ca_related(title, content, ca_kzkursiv_KEYWORDS)
                        if not matched_keywords:
                            logging.debug(f"Skipping non-relevant article: {title}")
                            continue
                        
                        article_details = {
                            "title": title,
                            "link": link,
                            "date": publication_date,
                            "content": content,
                            "keywords": matched_keywords,
                            "source": "Kursiv",
                            "region": "CentralAsia",
                            "sector": "banks"
                        }
                        save_article(article_details)
                        articles.append(article_details)
                        
                    except Exception as e:
                        print(f"Error extracting details for article '{title}': {e}")
        return articles
    return []


def uzkursiv_banks():
    url = "https://uz.kursiv.media/en/"

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'if-modified-since': 'Wed, 27 Nov 2024 07:31:06 GMT',
        'if-none-match': '"34204c95892e4fbdde241ce4e461a3ce"',
        'priority': 'u=0, i',
        'referer': 'https://uz.kursiv.media/en/guide/first-among-equal/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"131.0.6778.86"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.86", "Chromium";v="131.0.6778.86", "Not_A Brand";v="24.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
    except Exception as e:
        print(f"Error fetching main page {url}: {e}")
        return []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        article_cards = soup.select('.post-dynamic-card')
        for card in article_cards:
            title_tag = card.select_one('.post-dynamic-card__title a')
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag['href']

                try:
                    article_response = requests.get(link, headers=headers, timeout=30)
                except Exception as e:
                    print(f"Error fetching article {link}: {e}")
                    continue

                if article_response.status_code == 200:
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')
                    try:
                        publication_date = None
                        date_element = article_soup.select_one('.single-publishing-time__date')
                        if date_element and date_element.has_attr('datetime'):
                            raw_date = date_element['datetime']
                            if raw_date:
                                try:
                                    publication_date = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                                except ValueError:
                                    publication_date = raw_date[:10] if len(raw_date) >= 10 else None
                        
                        if publication_date is None:
                            try:
                                response = requests.get(url, headers=headers, timeout=30)
                                if response.status_code == 200:
                                    soup = BeautifulSoup(response.text, 'html.parser')
                                    script = soup.find('script', type='application/ld+json')
                                    if script:
                                        json_data = json.loads(script.string)
                                        date = json_data.get('datePublished')
                                        if date:
                                            try:
                                                publication_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                                            except ValueError:
                                                publication_date = date[:10] if len(date) >= 10 else None
                            except Exception as e:
                                print(f"Error in fallback date fetch: {e}")

                        tags = [tag.get_text(strip=True) for tag in article_soup.select('.tag-cloud__item')]
                        paragraphs = article_soup.select('.single-body p')
                        content = "\n\n".join(p.get_text(strip=True) for p in paragraphs)
                        matched_keywords = is_ca_related(title, content, ca_kzkursiv_KEYWORDS)
                        if not matched_keywords:
                            logging.debug(f"Skipping non-relevant article: {title}")
                            continue

                        article_details = {
                            "title": title,
                            "link": link,
                            "date": publication_date,
                            "content": content,
                            "keywords": matched_keywords,
                            "source": "Kursiv",
                            "region": "CentralAsia",
                            "sector": "banks"
                        }
                        save_article(article_details)
                        articles.append(article_details)
                    except Exception as e:
                        print(f"Error extracting details for article '{title}': {e}")
        return articles
    return []

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
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=30)
        if response.status_code == 200:
            return response.json()[0][0]
        else:
            print(f"Translation failed with status code {response.status_code}")
            return text
    except Exception as e:
        print(f"Translation request failed: {e}")
        return text

def uz_kursiv_insurance():
    url = "https://uz.kursiv.media/tag/strakhovanie/"
    headers = {
        'Referer': 'https://uz.kursiv.media/2025-01-20/v-uzbekistane-vnedryayut-rejting-strahovyh-kompanij/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
    except Exception as e:
        print(f"Error fetching insurance page: {e}")
        return []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article', class_='post post-category')
        extracted_articles = []
        for article in articles:
            date = article.find('time', class_='post-date').text.strip() if article.find('time', class_='post-date') else None
            title_tag = article.find('h2', class_='post-title').find('a')
            title = title_tag.text.strip() if title_tag else None
            article_url = title_tag['href'] if title_tag else None
            excerpt = article.find('div', class_='post-excerpt').text.strip() if article.find('div', class_='post-excerpt') else None
            translated_date = translate_text(date, source_lang="ru", target_lang="en") if date else None
            translated_title = translate_text(title, source_lang="ru", target_lang="en") if title else None
            translated_excerpt = translate_text(excerpt, source_lang="ru", target_lang="en") if excerpt else None
            articles_info = ({
                'date': translated_date,
                'title': translated_title,
                'link': article_url,
                'content': translated_excerpt,
                'source': 'Kursiv',
                'region': 'CentralAsia',
                'sector': 'banks',
                'keywords': None,
            })
            save_article(articles_info)
            extracted_articles.append(articles_info)
        return extracted_articles
    return []

def kursiv_articles():
    articles = kz_kursiv() + uzkursiv_banks() + uz_kursiv_insurance()

    return articles