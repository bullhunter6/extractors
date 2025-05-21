import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.db_utils import save_pub

def erm_pub():
    url = "https://www.erm.com/insights/?theme=Sustainability%20Institute"

    headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'TiPMix=29.847336111868692; x-ms-routing-name=self; ASP.NET_SessionId=5ttvxpin0wezaslshmqzl0og; ARRAffinity=06dece71727ab2c9a75506862155277ef8948b1004ad39e70a73eb837c7bf7ad; ARRAffinitySameSite=06dece71727ab2c9a75506862155277ef8948b1004ad39e70a73eb837c7bf7ad; _gcl_au=1.1.1957638557.1723008932; _gid=GA1.2.1457274674.1723008933; is=ef3286cf-d7f5-47b9-b757-f24f98b24738; iv=63d1c2f1-cd8c-445c-9eba-1ec332a7b9f6; ai_user=zXA0c|2024-08-07T05:35:33.145Z; _ga=GA1.1.390675091.1723008933; _uetsid=dd9c1950547e11efbd933b1fb36fb660; _uetvid=dd9c82d0547e11efb60179676201d6ca; _clck=25mml8%7C2%7Cfo4%7C0%7C1680; OptanonAlertBoxClosed=2024-08-07T05:35:34.519Z; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Aug+07+2024+09%3A35%3A34+GMT%2B0400+(Gulf+Standard+Time)&version=202306.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=579cb5f2-16e3-4730-a614-b62cca6da642&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1; _clsk=13fz9ec%7C1723008934941%7C1%7C1%7Cu.clarity.ms%2Fcollect; ai_session=bMYBF|1723008933847.4|1723009290950.5; _ga_65MSEV84N0=GS1.1.1723008933.1.1.1723009299.60.0.0',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
            }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = []
    insight_blocks = soup.find_all('div', class_='individual-insight-blocks')

    for block in insight_blocks:
        title_tag = block.find('h5', class_='card-title').a
        title = title_tag.text.strip()
        link = "https://www.erm.com" + title_tag['href']

        authors_tag = block.find('div', class_='insights-authors')
        summary = authors_tag.p.text.strip() if authors_tag else "Authors not found"

        date_tag = block.find('div', class_='insights-date')
        if date_tag:
            date_str = date_tag.p.text.strip()
            try:
                date_obj = datetime.strptime(date_str, "%d %B %Y")
                formatted_date = date_obj.strftime("%Y-%m-%d")
            except ValueError as ve:
                print(f"Error parsing date: {date_str}, due to {ve}")
                formatted_date = None
        else:
            formatted_date = None

        image_tag = block.find('div', class_='insight-image')
        image_url = "https://www.erm.com" + image_tag['data-src'] if image_tag else "Image not found"

        source = 'ERM Insights'

        article_data = {
            'title': title,
            'summary': summary,
            'date': formatted_date,
            'link': link,
            'image_url': image_url,
            'source': source
        }
        save_pub(article_data)
        articles.append(article_data)
    return articles