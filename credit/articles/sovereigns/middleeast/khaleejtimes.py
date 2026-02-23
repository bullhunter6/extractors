import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.check import me_related
from utils.db import save_article

sovereign_keywords =[#removed all countries names
    "IPO","sovereign rating",

    "Finance system","local goverment","goverment","goverment bonds","goverment spending","goverment budget",
    "goverment deficit","goverment surplus","goverment revenue","goverment expenditure","goverment fiscal policy","goverment monetary policy","goverment stimulus","goverment recovery",
    "goverment growth","goverment outlook","goverment impact","goverment contraction","goverment indicators","goverment rate cut","goverment mortgage","goverment mortgages",
    "goverment interest rate","goverment interest rates","goverment central bank","goverment central banks","goverment monetary policy","goverment fiscal policy",
    "goverment budget","goverment budgets","goverment deficit","goverment deficits","goverment government debt","goverment debt to GDP","goverment GDP","goverment GDP growth",
    "goverment economy","goverment economic","goverment economic growth","goverment economic outlook","goverment economic recovery","goverment economic stimulus",
    "goverment economic stimulus package","goverment economic impact","goverment economic contraction","goverment economic indicators","goverment rate cut",
    "goverment mortgage","goverment mortgages",'monetary policy','fiscal policy','goverment budget','goverment budgets','deficit',
    'deficits','government debt','debt to GDP','GDP growth',"economic growth","economic outlook","economic recovery","economic stimulus",
    "economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgage","mortgages","sukuk","economic growth","economic outlook",
    "economic recovery","economic stimulus","economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgage","mortgages",
]

def khaleejtimes_markets():
    url = "https://www.khaleejtimes.com/business/markets"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    articles=[]
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles_div = soup.find_all('article', class_=['listing-normal-teasers', 'listing-top-main-teaser'])

        for article in articles_div:
            title_tag = article.find('h2') or article.find('h3')
            link_tag = title_tag.find('a') if title_tag else None
            title = title_tag.text.strip() if title_tag else "No Title" 
            link = link_tag['href'] if link_tag else "No Link"

            if link and not link.startswith("http"):
                link = "https://www.khaleejtimes.com" + link

            try:
                content_response = requests.request("GET", link, headers=headers, timeout=30)
            except Exception as e:
                print(f"Error fetching article {link}: {e}")
                continue

            content = ""
            if content_response.status_code == 200:
                content_soup = BeautifulSoup(content_response.text, 'html.parser')
                content_div = content_soup.find('div', class_ = 'col-12 col-lg-9 col-md-9 details article-center-wrap-nf')
                if content_div:
                    content = content_div.get_text(strip=True)

                date_div = content_soup.find('div', class_='timestamp-latnw-nf')
                formatted_date = datetime.now().strftime("%Y-%m-%d")
                if date_div:
                    date_text = date_div.text.strip()
                    published_date_line = date_text.split('\n')[0]
                    import re
                    match = re.search(r"(\d{1,2}\s+\w{3}\s+\d{4})", published_date_line)
                    if match:
                        date = match.group(1)
                        formatted_date = datetime.strptime(date, "%d %b %Y").strftime("%Y-%m-%d")



                    matched_keywords = me_related(title, content, sovereign_keywords)
                    if not matched_keywords:
                        continue

                    if "india" in title.lower() or "Trump" in title:
                        continue

                    artricle_data = ({
                        "title": title,
                        "link": link,
                        "date": formatted_date,
                        "content": content,
                        "keywords": matched_keywords,
                        "source": "Khaleej Times",
                        "region": "MiddleEast",
                        "sector": "sovereigns",
                    })
                    save_article(artricle_data)
                    articles.append(artricle_data)
    return articles


def khaleejtimes_economy():
    url = "https://www.khaleejtimes.com/business/economy"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    articles=[]
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles_div = soup.find_all('article', class_=['listing-normal-teasers', 'listing-top-main-teaser'])

        for article in articles_div:
            title_tag = article.find('h2') or article.find('h3')
            link_tag = title_tag.find('a') if title_tag else None
            title = title_tag.text.strip() if title_tag else "No Title" 
            link = link_tag['href'] if link_tag else "No Link"

            if link and not link.startswith("http"):
                link = "https://www.khaleejtimes.com" + link

            try:
                content_response = requests.request("GET", link, headers=headers, timeout=30)
            except Exception as e:
                print(f"Error fetching article {link}: {e}")
                continue

            content = ""
            if content_response.status_code == 200:
                content_soup = BeautifulSoup(content_response.text, 'html.parser')
                content_div = content_soup.find('div', class_ = 'col-12 col-lg-9 col-md-9 details article-center-wrap-nf')
                if content_div:
                    content = content_div.get_text(strip=True)

                date_div = content_soup.find('div', class_='timestamp-latnw-nf')
                formatted_date = datetime.now().strftime("%Y-%m-%d")
                if date_div:
                    date_text = date_div.text.strip()
                    published_date_line = date_text.split('\n')[0]
                    import re
                    match = re.search(r"(\d{1,2}\s+\w{3}\s+\d{4})", published_date_line)
                    if match:
                        date = match.group(1)
                        formatted_date = datetime.strptime(date, "%d %b %Y").strftime("%Y-%m-%d")


                    matched_keywords = me_related(title, content, sovereign_keywords)
                    if not matched_keywords:
                        continue
                    # also exclude articles with india and indian in title and content
                    if "india" in title.lower():
                        continue
                    artricle_data = ({
                        "title": title,
                        "link": link,
                        "date": formatted_date,
                        "content": content,
                        "keywords": matched_keywords,
                        "source": "Khaleej Times",
                        "region": "MiddleEast",
                        "sector": "sovereigns",
                    })
                    save_article(artricle_data)
                    articles.append(artricle_data)
    return articles


def khaleejtimes_sov():
    articles = khaleejtimes_markets() + khaleejtimes_economy()
    return articles
