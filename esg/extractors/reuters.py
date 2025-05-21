import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
from utils.check import is_esg_related
import logging
from utils.db_utils import save_article

def reuters_articles():
    url = "https://www.reuters.com/sustainability/"
    headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-US,en;q=0.9',
      'cookie': 'ajs_anonymous_id=edff1d6d-8577-4bb7-b05f-bda5abe22072; usprivacy=1---; permutive-id=8589f72b-2da9-4604-bec1-358509310be8; OneTrustWPCCPAGoogleOptOut=false; cleared-onetrust-cookies=Thu, 17 Feb 2022 19:17:07 GMT; datadome=8IdjbpOCJGl3Kb_ekvQb0oRmEf8~zreGXSWk_W7E8BSwwgOc0pPr__7A66wDlRwKfVELQ4ulFMOU0KsG2yS42NcH8FYmjyM6FzygFuC4jEGQcAftgBIJyUFNz8tEAvAq; _lr_geo_location_state=DU; _lr_geo_location=AE; _pbjs_userid_consent_data=3524755945110770; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.reuters.com%252F; ABTasty=uid=3vqjhhdszyw8s446; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Nov+18+2024+17%3A58%3A33+GMT%2B0400+(Gulf+Standard+Time)&version=202408.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=0e02e297-d22a-4592-8312-b9d34064aa67&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=1%3A1%2C3%3A1%2CSSPD_BG%3A1%2C4%3A1%2C2%3A1&AwaitingReconsent=false; reuters-geo={"country":"-", "region":"-"}; reuters-geo={"country":"-", "region":"-"}',
      'if-modified-since': 'Mon, 18 Nov 2024 13:33:32 GMT',
      'if-none-match': 'W/"147a45-rkAOsLKpQSGfos9ldykETWrxyBU"',
      'priority': 'u=0, i',
      'referer': 'https://www.reuters.com/',
      'sec-ch-device-memory': '8',
      'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
      'sec-ch-ua-arch': '"x86"',
      'sec-ch-ua-full-version-list': '"Chromium";v="130.0.6723.117", "Google Chrome";v="130.0.6723.117", "Not?A_Brand";v="99.0.0.0"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-model': '""',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', id='fusion-metadata', type='application/javascript')

        if script_tag:
            script_content = script_tag.string
            start_index = script_content.find('Fusion.globalContent=') + len('Fusion.globalContent=')
            end_index = script_content.find(';', start_index)
            json_data = script_content[start_index:end_index].strip()
            try:
                data = json.loads(json_data)
                articles = data.get('result', {}).get('articles', [])
                extracted_articles = []
                for article in articles:
                    title = article.get('title')
                    link = f"https://www.reuters.com{article.get('canonical_url')}"
                    published_time = article.get('published_time', 'No publish time available.')
                    date = datetime.strptime(published_time.replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f")
                    formatted_date = date.strftime('%Y-%m-%d')
                    paragraphs = []
                    response = requests.get(link, headers=headers)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        article_body = soup.find('div', {'data-testid': 'ArticleBody'})
                        paragraphs = []
                        if article_body:
                            paragraphs = [p.get_text(strip=True) for p in article_body.find_all('div', {'data-testid': lambda x: x and x.startswith('paragraph-')})]
                    matched_keywords = is_esg_related(title, paragraphs)
                    if not matched_keywords:
                        logging.debug(f"Skipping non-relevant article: {title}")
                        continue
                    articles = []
                    extracted_articles = ({
                        'title': title,
                        'url': link,
                        'summary': paragraphs,
                        'date': formatted_date,
                        'source': 'Reuters',
                        'keywords': matched_keywords
                    })
                    save_article(extracted_articles)
                    articles.append(extracted_articles)

                return extracted_articles
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        else:
            print("Script tag not found.")