import requests
from bs4 import BeautifulSoup
from utils.db_utils import save_article
from datetime import datetime
from utils.keywords import ESG_KEYWORDS
import logging


def parse_date(date_string):
    try:
        date_string = date_string.replace("Published: ", "")
        return datetime.strptime(date_string, "%a %d %b %Y, %I:%M %p")
    except ValueError as e:
        print("Date parsing error:", e)
        return None

def is_esg_related(title, summary):
    content = title.lower() + " " + summary.lower()
    matched_keywords = [keyword for keyword in ESG_KEYWORDS if keyword.lower() in content]
    return matched_keywords

def khaleejtimes_articles():
    url = "https://www.khaleejtimes.com/wp-admin/admin-ajax.php"
    payload = "action=get_section_listing&pagenr=&limit=20&sub_section=energy&section=business"
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'visid_incap_1773870=jTfFqwH5TOqMe5PeX9zRx/v9RmYAAAAAQUIPAAAAAADfYE/LU8r826cONMMtT0Ut; user_sessions_executed=done; random_user=2; random_user_widget=0; gsi_session=1; nlbi_1773870=V7d9F/DqbkfIhbpjVzlQLAAAAAD+0WKMpWRJ6fxldF9pygKC; incap_ses_1166_1773870=clqZZf9BBEgZdiId+nYuECuANGcAAAAA7hGpobWm00uHUZZy2NNm6g==; adblock_detection=done; boxx_token_id_kt=a99efd25300e-4071ebab8072-71f451cd4d07-f8c36e014088; uid_dm=a2e96af3-d643-7274-da0d-bf2a7161de08; user_sessions=3; incap_ses_1166_1773870=G1NYGBDeakVC4E0d+nYuEPqiNGcAAAAAy5lz2Rk0/srVSHs0CS5S+g==; visid_incap_1773870=LPw06ZDMS9i/GYLruvNx+5kDeWYAAAAAQUIPAAAAAAD/V6sxJScc4n5qsmVmotvd; boxx_token_id_kt=e220b3806500-cb82e11c7794-3d715f4d5233-dfe79b3f9e9d',
        'origin': 'https://www.khaleejtimes.com',
        'priority': 'u=0, i',
        'referer': 'https://www.khaleejtimes.com/business/energy',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.post(url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles_url = soup.find_all("article", class_="listing-normal-teasers card-article-list-item")
    articles = []
    for article in articles_url:
        title_tag = article.find("h3")
        link_tag = title_tag.find("a") if title_tag else None
        if link_tag:
            title = link_tag.get_text(strip=True)
            url = link_tag['href']
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "No title found"
            timestamp_div = soup.find("div", class_="timestamp-latnw-nf")
            published_date_text = timestamp_div.find_all("p")[0].get_text(strip=True) if timestamp_div and len(timestamp_div.find_all("p")) > 0 else "No published date found"
            published_date = parse_date(published_date_text) if published_date_text != "No published date found" else None
            article_body_divs = soup.find_all("p")
            article_body = "\n\n".join([p.get_text(strip=True) for p in article_body_divs if p.get_text(strip=True)])

            matched_keywords = is_esg_related(title, article_body)
            if not matched_keywords:
                logging.debug(f"Skipping non-relevant article: {title}")
                continue

            article_data = {    
                'title': title,
                'url': url,
                'date': published_date,
                'summary': article_body,
                'source': 'Khaleej Times',
                'keywords': matched_keywords
            }
            save_article(article_data)
            articles.append(article_data)
    return articles