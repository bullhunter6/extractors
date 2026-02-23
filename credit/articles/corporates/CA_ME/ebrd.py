import requests
from bs4 import BeautifulSoup
from dateutil import parser
from utils.check import filter_articles_by_region_2
from utils.keywords import CP_COMMON_KEYWORDS, REGIONAL_KEYWORDS, CP_RARE_KEYWORDS
from utils.db import save_article
from datetime import datetime

def ebrd():
    url = "https://www.ebrd.com/news"

    headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'Accept-Language': 'en-US,en;q=0.9',
      'Cache-Control': 'max-age=0',
      'Connection': 'keep-alive',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'none',
      'Sec-Fetch-User': '?1',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'Cookie': 'waf_mgt_id=AAI7HOZjZztp9AAAAAAAADubZiQFBAMM6_UzO8tDWehd2QNmg2_qz8AxD4JiWeedOw==VepjZw==CEr-G4yYGJtM6v5jtMZ-k6yLONw=; waf_mgt_id_.ebrd.com_%2F_wat=AAAAAAWRwpX7UPVh_kZmyIOhdoAsDqhGdW5jjaPTZAlbL5BeP-sPRx0aQaQEFZNO_vKXm9MWmPZSJ-hMPHba7pC8da0Z#wxL6m4tB8luYaqVYQ6pmVtdw9M0A&; bot_mgt_id=MDMBAAIAm-qCSQAAAAAFHsO7HOZjZwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD71xQtOIryuy_tIxL1DJE-taJ7m'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        news_posts = soup.find_all("div", class_="col-xs-12 col-sm-4 col-md-4 col-lg-4 post news-post")
        news = []
        for post in news_posts:
            date_tag = post.find("dt")
            date_str = date_tag.get_text(strip=True) if date_tag else None

            if date_str:
                try:
                    # Explicitly define format (DD.MM.YY)
                    parsed_date = datetime.strptime(date_str, "%d.%m.%y")  
                    formatted_date = parsed_date.strftime("%Y-%m-%d")  # Convert to YYYY-MM-DD
                except ValueError:
                    formatted_date = "Invalid date"
            else:
                formatted_date = "No date"

            link_tag = post.find("a", href=True)
            title = link_tag.get_text(strip=True) if link_tag else "No title"
            link = link_tag["href"] if link_tag and link_tag.has_attr("href") else "No link"
            content_response = requests.get(link, headers=headers)
            if content_response.status_code == 200:
                soup = BeautifulSoup(content_response.text, "html.parser")
                article = soup.find("article")
                content_parts = []
                if article:
                    paragraphs = article.find_all("p")
                    for p in paragraphs:
                        text = p.get_text(strip=True)
                        if text:
                            content_parts.append(text)
                    list_items = article.find_all("li")
                    for li in list_items:
                        text = li.get_text(strip=True)
                        if text:
                            content_parts.append(text)
                article_content = "\n".join(content_parts)
            region, keywords = filter_articles_by_region_2(
                        title, article_content, CP_COMMON_KEYWORDS, REGIONAL_KEYWORDS, CP_RARE_KEYWORDS
                    )
            if keywords:
                news_data=({
                    "date": formatted_date,
                    "title": title,
                    "link": link,
                    "content": article_content,
                    "region": region,
                    "keywords": keywords,
                    "sector": "corporates",
                    'source': 'EBRD'
                })
                save_article(news_data)
                news.append(news_data)
    return news