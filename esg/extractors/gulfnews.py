import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from utils.db_utils import save_article
from utils.check import is_esg_related

def gulfnews_articles():
    url = "https://gulfnews.com/business/energy"
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'VISITOR=returning; NEW_VISITOR=new; VISITOR=returning; NEW_VISITOR=new; visid_incap_1101165=9YkEsPrfTuWnf0krc3W9W7qkaWYAAAAAQUIPAAAAAABFXbFJzEHVp5GZ0Dh88SEz; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAEzIEYOAmATgFYA7BwAsABgDMY7qP4j%2BANg4gAvkA; _pcid=%7B%22browserId%22%3A%22lxbvlvxc9kxqsogm%22%7D; _pcus=eyJ1c2VyU2VnbWVudHMiOnsiQ09NUE9TRVIxWCI6eyJzZWdtZW50cyI6WyJMVHM6MjA3NzI5ZjM0ODlhMjIwY2NkZTAxZTUyODY4Y2QzNzdjNTkxYmUzZTpub19zY29yZSJdfX19; nlbi_1101165=JhlMDI86MVum3e1PdvUcAAAAAAAybnmPKWq7hiTzT5tjoZFA; __pat=14400000; NEW_VISITOR=new; incap_ses_1807_1101165=57z+Kx3aVlPI51MV9MATGaquNGcAAAAA9zB6evaAm/1GL+k6eilLEQ==; ALNISRGNX=7B5262BB2A9B68DA180157F5970E227B; __pvi=eyJpZCI6InYtbTNmeTJmaGhtaWEzdXQ4MSIsImRvbWFpbiI6Ii5ndWxmbmV3cy5jb20iLCJ0aW1lIjoxNzMxNTA2MTcwMDg1fQ%3D%3D; __tbc=%7Bkpex%7DsmpHRpAdJ_ySNbGqi-Ry_m4ZINdXrbeqOWEtRkBs2icaTneH4hhN1KNuLH04zvyi; xbc=%7Bkpex%7DkMjg4jO7QoPlyNbmgJW7kye9rbtkUkYRp0nHDIdVS1AsB38coSDzpWK69fBWgFMGTJr9xSXrh5lME0RedHeCrA; VISITOR=returning; NEW_VISITOR=new; ALNISRGNX=2497044055DB05F963A8A9439AF734F3',
    'If-Modified-Since': 'Wed, 13 Nov 2024 13:54:57 GMT',
    'Referer': 'https://gulfnews.com/business',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    content_wrapper = soup.find("div", class_="content-wrapper")
    articles = []

    if content_wrapper:
        cards = content_wrapper.find_all("div", class_="card")
        for card in cards:
            title_tag = card.find("h2", class_="card-title")
            if title_tag and title_tag.find("a"):
                title = title_tag.get_text(strip=True)
                relative_url = title_tag.find("a")["href"]
                article_url = "https://gulfnews.com" + relative_url
                
                response = requests.get(article_url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find("h1", {"data-article-head": True}).get_text(strip=True) if soup.find("h1", {"data-article-head": True}) else "No title found"

                date_tag = soup.find("time", class_="publish")
                publish_date = date_tag.get_text(strip=True) if date_tag else "No publish date found"
                date_string = publish_date.replace("Published:", "").strip()
                parsed_date = datetime.strptime(date_string, "%B %d, %Y %H:%M")
                formatted_date = parsed_date.strftime("%Y-%m-%d")

                body_content = []
                article_body = soup.find("div", class_="article-body")
                if article_body:
                    paragraphs = article_body.find_all("p")
                    for paragraph in paragraphs:
                        body_content.append(paragraph.get_text(strip=True))
                article_body_text = "\n\n".join(body_content)
                matched_keywords = is_esg_related(title, article_body_text)
                if not matched_keywords:
                    logging.debug(f"Skipping non-relevant article: {title}")
                    continue
                articles_data = {
                    "title": title,
                    "date": formatted_date,
                    "url": article_url,
                    "summary": article_body_text,
                    "source": "Gulf News",
                    "keywords": matched_keywords
                }
                save_article(articles_data)
                articles.append(articles_data)
    return articles
