import requests
from bs4 import BeautifulSoup
from dateutil import parser
from utils.check import filter_articles_by_region_2
from utils.keywords import COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS
from utils.db import save_article

def get_article_content(url):
    try:
        payload = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

        response = requests.get(url, headers=headers, data=payload)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            content = ""

            main_content_divs = soup.find_all('div', class_=['up-rich-text__container-content', 'richText-content cmp-text nested-tile--georgia-font'])

            for div in main_content_divs:
                paragraphs = div.find_all(['p', 'li', 'ol'])
                for paragraph in paragraphs:
                    text = paragraph.get_text(strip=True)
                    if not any(unwanted in text.lower() for unwanted in [
                        "see more", "ey helps", "extraordinary people", "build a better working world",
                        "long-term value", "read more", "read less", "discover", "explore"
                    ]):
                        content += text + "\n"
                        content = "\n".join([line.strip() for line in content.split("\n") if line.strip()])

            formatted_date = None
            date_div = soup.find('div', class_='up-display-metadata-utility')
            if date_div:
                date_parts = [part.strip() for part in date_div.text.split('\n') if part.strip()]
                date = date_parts[-1] if date_parts else "Date not found"
                try:
                    formatted_date = parser.parse(date).strftime("%Y-%m-%d")
                except Exception:
                    formatted_date = "Invalid date format"

            return content, formatted_date

    except Exception as e:
        print(f"Error fetching content for {url}: {str(e)}")
        return "Error fetching content", "Error fetching date"

    return "Content not available", "Date not available"

def ey_articles():
    url = "https://www.ey.com/en_gl/industries/banking-capital-markets"

    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers, data=payload)
    articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        featured_articles = soup.find_all('div', class_='up-hero-banner-image')
        if featured_articles:
            title = featured_articles[0].find('h3').text.strip()
            link = featured_articles[0].find('a')['href']
            full_link = f"https://www.ey.com{link}"
            featured_content, featured_date = get_article_content(full_link)
            if title and full_link and featured_content and featured_date:
                region, keywords = filter_articles_by_region_2(title, featured_content, COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS)
                if keywords:
                    articles_info = ({
                        'title': title,
                        'link': full_link,
                        'content': featured_content,
                        'date': featured_date,
                        'region': region,
                        'keywords': keywords,
                        'sector': 'banks',
                        'source': 'EY'
                    })
                    save_article(articles_info)
                    articles.append(articles_info)

        thinking_articles = soup.find_all('div', class_='up-content-grid__list-item-details')
        for article in thinking_articles:
            try:
                thinking_title = article.find('p', class_="up-content-grid__list-item-title").text.strip()
                thinking_link = article.find('a')['href']
                thinking_full_link = f"https://www.ey.com{thinking_link}"
                thinking_content, thinking_date = get_article_content(thinking_full_link)
                if thinking_title and thinking_full_link and thinking_content and thinking_date:
                    region, keywords = filter_articles_by_region_2(
                        thinking_title, thinking_content, COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS
                    )
                    if keywords:
                        articles_info2 = ({
                            'title': thinking_title,
                            'link': thinking_full_link,
                            'content': thinking_content,
                            'date': thinking_date,
                            'region': region,
                            'keywords': keywords,
                            'sector': 'banks',
                            'source': 'EY'
                        })
                        save_article(articles_info2)
                        articles.append(articles_info2)
            except Exception as e:
                print(f"Error parsing article details: {str(e)}")

    return articles