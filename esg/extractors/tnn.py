import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re
import logging
from utils.keywords import ESG_KEYWORDS
from utils.db_utils import save_article
from utils.check import is_esg_related

def tnn_articles():
    url = "https://www.thenationalnews.com/pf/api/v3/content/fetch/story-feed-sections?query=%7B%22feedOffset%22%3A0%2C%22feedSize%22%3A20%2C%22includeSections%22%3A%22%2Fclimate%2Fenvironment%22%7D&d=841&_website=the-national"
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'arc-geo={"country_code":"AE","city":"DUBAI","longitude":"55.28","latitude":"25.25"}; OptanonAlertBoxClosed=2024-07-23T06:10:42.312Z; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAEzIFYAObgFgHZeAJgBsARl5cAnCP5CAzDxABfIA; _pprv=eyJjb25zZW50Ijp7IjAiOnsibW9kZSI6Im9wdC1pbiJ9LCIxIjp7Im1vZGUiOiJvcHQtaW4ifSwiMiI6eyJtb2RlIjoib3B0LWluIn0sIjMiOnsibW9kZSI6Im9wdC1pbiJ9LCI0Ijp7Im1vZGUiOiJvcHQtaW4ifSwiNSI6eyJtb2RlIjoib3B0LWluIn0sIjciOnsibW9kZSI6Im9wdC1pbiJ9fSwicHVycG9zZXMiOnsiMCI6IkFNIiwiMSI6IkFEIiwiMiI6IkNQIiwiMyI6IlBSIiwiNCI6IlBSIiwiNSI6IlBSIiwiNyI6IkRMIn19; _pcid=%7B%22browserId%22%3A%22m35oi9zkzbpuwhhi%22%7D; __pat=14400000; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Nov+14+2024+09%3A12%3A57+GMT%2B0400+(Gulf+Standard+Time)&version=202409.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=22c0fc02-0652-4a4d-9842-cbb05da5230c&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0005%3A1&intType=1&geolocation=AE%3BDU&AwaitingReconsent=false; __tbc=%7Bkpex%7DOmLuA6U44GTK8wu0eHaGXsApTiP_bcJv-QINTe0_c0TBwlSq5T1pca2i729du_Ar; xbc=%7Bkpex%7DYzJcOHrEayGlt3sQKbGXgXcgY-zSvrAoraiMiEFLrrvcCRH-3U62TPXEJfboK8BXhRdYB90lnyuG1FRtj9P29rg33qhfpub1oAulACEdKbA; __pvi=eyJpZCI6InYtbTNneTZrenhxaXV0bm84aSIsImRvbWFpbiI6Ii50aGVuYXRpb25hbG5ld3MuY29tIiwidGltZSI6MTczMTU2NjgzMDAyOX0%3D; arc-geo={"country_code":"AE","city":"DUBAI","longitude":"55.28","latitude":"25.25"}',
        'if-modified-since': '1731547224832',
        'priority': 'u=1, i',
        'referer': 'https://www.thenationalnews.com/climate/environment/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    articles_list = data.get("content_elements", [])
    if not articles_list:
        logging.warning("No articles found in the API response.")
        return []
    
    articles = []
    for article in articles_list:
        title = article.get("headlines", {}).get("basic", "No title available")
        display_date = article.get("display_date", "")

        if display_date:
            display_date = display_date.split(".")[0]
            try:
                formatted_date = datetime.fromisoformat(display_date.replace("Z", "")).strftime("%Y-%m-%d")
            except ValueError:
                logging.error(f"Date parsing failed for: {display_date}")
                formatted_date = "Invalid date format"
        else:
            formatted_date = "No date available"
        
        canonical_url = article.get("canonical_url", "")
        full_link = f"https://www.thenationalnews.com{canonical_url}"
        logging.debug(f"Processing article: {title} - {full_link}")
        article_response = requests.get(full_link, headers=headers)
        soup = BeautifulSoup(article_response.text, 'html.parser')
        
        script_tag = soup.find("script", id="fusion-metadata")
        full_article_text = "No article content found"
        
        if script_tag and script_tag.string:
            json_match = re.search(r'Fusion\.globalContent=({.*?});\s*Fusion', script_tag.string, re.DOTALL)
            if json_match:
                json_data = json_match.group(1)
                try:
                    data = json.loads(json_data)
                    content_elements = data.get("content_elements", [])
                    article_content = []
                    
                    for element in content_elements:
                        if element.get("type") == "text":
                            article_content.append(element.get("content", "").strip())
                    
                    full_article_text = "\n\n".join(article_content)
                except json.JSONDecodeError:
                    logging.error("Error decoding article content JSON.")
            else:
                logging.warning("No JSON content found in the article's script tag.")
        
        matched_keywords = is_esg_related(title, full_article_text)
        if not matched_keywords:
            logging.debug(f"Skipping non-relevant article: {title}")
            continue

        article_data = {
            "title": title,
            "date": formatted_date,
            "url": full_link,
            "summary": full_article_text,
            "source": "The National News",
            "keywords": matched_keywords
        }
        save_article(article_data)
        articles.append(article_data)
    
    return articles
