import requests
from bs4 import BeautifulSoup
from utils.check import filter_articles_by_region_2
from utils.keywords import COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS
from utils.db import save_article
from dateutil import parser

def bcg():
    base_url = "https://www.bcg.com/search"
    headers = {
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
      'priority': 'u=1, i',
      'referer': 'https://www.bcg.com/search?q=&f7=00000171-f177-d0c2-a57d-fbff70ae0000',
      'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
    }

    articles = []

    for page in range(1, 5):
        params = {
            'q': '',
            'f7': '00000171-f177-d0c2-a57d-fbff70ae0000',
            'p': page
        }

        try:
            response = requests.get(base_url, headers=headers, params=params)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                results = soup.select('a.result-link')

                for result_link in results:
                    try:
                        link = result_link.get('href')
                        
                        # Extract title
                        title_tag = result_link.find('h2', class_='title')
                        title = title_tag.get_text(strip=True) if title_tag else ""
                        
                        # Extract date
                        date_div = result_link.find('div', class_='subtitle')
                        article_date = date_div.get_text(strip=True) if date_div else "Date not found"
                        
                        # Extract content/intro
                        content_div = result_link.find('div', class_='result-content')
                        article_content = content_div.get_text(strip=True) if content_div else ""

                        if title and link and article_date and article_content:
                            region, keywords = filter_articles_by_region_2(
                                title, article_content, COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS
                            )
                            
                            try:
                                formatted_date = parser.parse(article_date).strftime('%Y-%m-%d')
                            except:
                                formatted_date = article_date

                            if keywords:
                                articles_info = ({
                                    'title': title,
                                    'link': link,
                                    'date': formatted_date,
                                    'content': article_content,
                                    'region': region,
                                    'keywords': keywords,
                                    'sector': 'banks',
                                    'source': 'BCG'
                                })
                                save_article(articles_info)
                                articles.append(articles_info)

                    except Exception as e:
                        print(f"Error processing article: {e}")
                        continue
            else:
                print(f"Failed to fetch page {page}. Status: {response.status_code}")
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            
    return articles