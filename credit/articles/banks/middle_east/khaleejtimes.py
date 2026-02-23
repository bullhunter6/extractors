import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.check import me_related
from utils.keywords import me_kj_KEYWORDS
from utils.db import save_article


def khaleejtimes_articles():
    url = "https://www.khaleejtimes.com/business/finance"
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
                
            if content_response.status_code == 200:
                content_soup = BeautifulSoup(content_response.text, 'html.parser')
                content_div = content_soup.find('div', class_ = 'col-12 col-lg-9 col-md-9 details article-center-wrap-nf')
                content = ""
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


                    matched_keywords = me_related(title, content, me_kj_KEYWORDS)
                    if not matched_keywords:
                        continue
                    artricle_data = ({
                        "title": title,
                        "link": link,
                        "date": formatted_date,
                        "content": content,
                        "keywords": matched_keywords,
                        "source": "Khaleej Times",
                        "region": "MiddleEast",
                        "sector": "banks",
                    })
                    save_article(artricle_data)
                    articles.append(artricle_data)
    return articles





