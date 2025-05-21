import requests
from bs4 import BeautifulSoup
from utils.db_utils import save_article 

def sustainalytics_articles():
    url = "https://www.sustainalytics.com/esg-news"

    main_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'sf-data-intell-subject=1727087948762-4ef5e27a-d25e-4637-ac8e-787512e68589; sf-prs-ss=638626847488270000; sf-prs-lu=https://www.sustainalytics.com/; messagesUtk=9e77a6dbc2a84b39b0adfd1d8f6d7d7d; sf_abtests=6d9de14d-d722-452d-99af-702de9dbebc1; _cfuvid=xvaq7D5q5aJrTqKRCgQUTqFKb_JD920h1g2_BjtlqrY-1731930389083-0.0.1.1-604800000; sf-ins-ssid=1731930392460-adb4bb5c-5c82-4c43-842a-fc98991c2465; sf-ins-pv-id=68e7785e-b11c-4235-ac69-e4222cf70c88',
    'if-modified-since': 'Mon, 18 Nov 2024 09:03:06 GMT',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }
    sum_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'sf-data-intell-subject=1727087948762-4ef5e27a-d25e-4637-ac8e-787512e68589; sf-prs-ss=638626847488270000; sf-prs-lu=https://www.sustainalytics.com/; messagesUtk=9e77a6dbc2a84b39b0adfd1d8f6d7d7d; sf_abtests=6d9de14d-d722-452d-99af-702de9dbebc1; _cfuvid=xvaq7D5q5aJrTqKRCgQUTqFKb_JD920h1g2_BjtlqrY-1731930389083-0.0.1.1-604800000; sf-ins-ssid=1731930392460-adb4bb5c-5c82-4c43-842a-fc98991c2465; sf-ins-pv-id=e598aa6a-aa65-4a21-a22d-10c80e648bac',
        'priority': 'u=0, i',
        'referer': 'https://www.sustainalytics.com/esg-news',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=main_headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news_section = soup.find('div', class_='sust-news-list')

        if news_section:
            articles = []
            for item in news_section.find_all('li'):
                date_div = item.find('div', class_='sust-news-head text-muted')
                title_h3 = item.find('h3', class_='sust-news-title')
                link_a = title_h3.find('a') if title_h3 else None
                summary_p = item.find('p', class_='sust-news-summary')
                if date_div and title_h3 and link_a and summary_p:
                    date = date_div.text.strip()
                    title = title_h3.text.strip()
                    link = link_a['href']
                    response = requests.get(link, headers=sum_headers)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        main_content = soup.find('main', id='Contentplaceholder1_T3797DFBC039_Col00')
                        paragraphs = main_content.find_all('p') if main_content else []
                        summary = ' '.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                    articles_data = ({
                        'date': date,
                        'title': title,
                        'url': link,
                        'summary': summary,
                        "source": "Sustainalytics",
                        "keywords": None
                    })
                    save_article(articles_data)
                    articles.append(articles_data)
            return articles
