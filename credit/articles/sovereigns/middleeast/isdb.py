import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.check import me_related
from utils.db import save_article

sovereign_keywords =[
    "sovereign","sovereign rating","UAE", "United Arab Emirates", "Saudi Arabia", "GCC countries", "GCC", "Kuwait", "Oman", "Bahrein", "Qatar", "Dubai", "Abu Dhabi","KSA", "saudi", 
    "Middle east", "RAK","Sharjah", "Ras Al Khamiah","Gulf Cooperation Council","Persian Gulf", "Islamic Cooperation", "Arab League","Muscat","Red Sea", "Yemen", "Jordan", 
    "MENA", "OPEC", "Organization of the Petroleum Exporting Countries", "Arabic Gulf", "Arabian Sea",
    
    "Finance system","local goverment","goverment","goverment bonds","goverment spending","goverment budget",
    "goverment deficit","goverment surplus","goverment revenue","goverment expenditure","goverment fiscal policy","goverment monetary policy","goverment stimulus","goverment recovery",
    "goverment growth","goverment outlook","goverment impact","goverment contraction","goverment indicators","goverment rate cut","goverment mortgage","goverment mortgages",
    "goverment interest rate","goverment interest rates","goverment central bank","goverment central banks","goverment monetary policy","goverment fiscal policy",
    "goverment budget","goverment budgets","goverment deficit","goverment deficits","goverment government debt","goverment debt to GDP","goverment GDP","goverment GDP growth",
    "goverment economy","goverment economic","goverment economic growth","goverment economic outlook","goverment economic recovery","goverment economic stimulus",
    "goverment economic stimulus package","goverment economic impact","goverment economic contraction","goverment economic indicators","goverment rate cut",
    "goverment mortgage","goverment mortgages",'interest rate','interest rates','monetary policy','fiscal policy','goverment budget','goverment budgets','deficit',
    'deficits','government debt','debt to GDP','GDP','GDP growth',"economic growth","economic outlook","economic recovery","economic stimulus",
    "economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgage","mortgages","sukuk","economic growth","economic outlook",
    "economic recovery","economic stimulus","economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgage","mortgages",
]

def isdb_sov():
    url = "https://www.isdb.org/news?page=0"

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.isdb.org/news?page=1',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    articles = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles_divs = soup.find_all('div', class_='field-title')

        for div in articles_divs:
            a_tag = div.find('a')
            if a_tag:
                link = a_tag['href']
                full_link = f"https://www.isdb.org{link}"
                title = a_tag.text.strip()
                content_response = requests.get(full_link, headers=headers)
                if content_response.status_code == 200:
                    content_soup = BeautifulSoup(content_response.text, 'html.parser')
                    date_div = content_soup.find(
                        'div',
                        class_='date node-authored-on field field--name-isdb-node-authored-on field--type-x-node field--label-hidden field--item'
                    )
                    if date_div:
                        date_element = date_div.find('time')
                        if date_element:
                            date = date_element.text.strip()
                            formatted_date = datetime.strptime(date, "%d %B %Y").strftime("%Y-%m-%d")
                    else:
                        formatted_date = "No Date Available"

                    content_div = content_soup.find(
                        'div',
                        class_='field field--name-field-text field--type-text-long field--label-hidden field--item'
                    )
                    if content_div:
                        content = content_div.get_text(strip=True)
                    else:
                        content = "No Content Available"
                    matched_keywords = me_related(title, content, sovereign_keywords)
                    if not matched_keywords:
                        continue
                    artricle_data = ({
                        "title": title,
                        "link": full_link,
                        "date": formatted_date,
                        "content": content,
                        "keywords": matched_keywords,
                        "source": "Islamic State Bank",
                        "region": "MiddleEast",
                        "sector": "sovereigns",
                    })
                    save_article(artricle_data)
                    articles.append(artricle_data)
    return articles



