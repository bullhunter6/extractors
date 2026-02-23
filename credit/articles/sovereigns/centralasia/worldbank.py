import requests
from datetime import datetime
from utils.check import is_ca_related
from utils.db import save_article

sovereign_keywords =[
    "sovereign","sovereign rating","private sector","public sector",
    
    "Asia and Pacific", "Central Asia","Azerbaijan","Armenia","Turkmenistan","Kyrgyzstan","Tajikistan","Kazakhstan","Uzbekistan",
    "Silk Road","Caspian Sea","Eurasia", "Post-Soviet States","Samarkand","Economic Cooperation Organization","Silk Route",
    
    "privatisation","Finance system","local goverment","goverment","goverment bonds","goverment spending","goverment budget",
    "goverment deficit","goverment surplus","goverment revenue","goverment expenditure","goverment fiscal policy","goverment monetary policy","goverment stimulus","goverment recovery",
    "goverment growth","goverment outlook","goverment impact","goverment contraction","goverment indicators","goverment rate cut","goverment mortgage","goverment mortgages",
    "goverment interest rate","goverment interest rates","goverment central bank","goverment central banks","goverment monetary policy","goverment fiscal policy",
    "goverment budget","goverment budgets","goverment deficit","goverment deficits","goverment government debt","goverment debt to GDP","goverment GDP","goverment GDP growth",
    "goverment economy","goverment economic","goverment economic growth","goverment economic outlook","goverment economic recovery","goverment economic stimulus",
    "goverment economic stimulus package","goverment economic impact","goverment economic contraction","goverment economic indicators","goverment rate cut",
    "goverment mortgage","goverment mortgages",'interest rate','interest rates','monetary policy','fiscal policy','goverment budget','goverment budgets','budget deficit',
    'deficits','government debt','debt to GDP','GDP','GDP growth',"economy","economic growth","economic outlook","economic recovery","economic stimulus",
    "economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgage","mortgages","sukuk","economic growth","economic outlook",
    "economic recovery","economic stimulus","economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgage","mortgages","investments"
]

def wb_uzb():
    url = "https://search.worldbank.org/api/v2/news?format=json&rows=20&fct=displayconttype_exact,topic_exact,lang_exact,count_exact,countcode_exact,admreg_exact&src=cq55&apilang=en&lang_exact=English&count_exact=Uzbekistan&os=0"

    payload = {}
    headers = {
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'en-US,en;q=0.9',
      'content-length': '0',
      'content-type': 'text/plain',
      'origin': 'https://www.worldbank.org',
      'priority': 'u=1, i',
      'referer': 'https://www.worldbank.org/',
      'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      'Cookie': '__cf_bm=aPH37XQ4NoLNn_UmzVcUKfHtviVwrA.Sta0x1ouy_qw-1732788147-1.0.1.1-.cjUaqE4nydJYE7sULmfNZVkmQHERph2vTNuJv.UxDJ7K3_jTR33yqDkDK2VpyY4qM3nBPoRNBMqYCP_c4e1vg; search.worldbank.org=4649dbe96dd468ec6356e8c1410cda31; search.worldbank.orgCORS=4649dbe96dd468ec6356e8c1410cda31'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    elements = data.get("documents").values()
    articles = []
    for element in elements:
        title_tag = element.get("title")
        if title_tag is not None:
            title = title_tag.get("cdata!")

        link = element.get("url")

        date = element.get("lnchdt")
        if date is not None:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")


        content_tag = element.get("content")
        if content_tag is not None:
            content = content_tag.get("cdata!")
        matched_keywords = is_ca_related(title, content, sovereign_keywords)
        if not matched_keywords and link is None:
            continue
        if link and link.strip():
            artricle_data = {
                "title": title,
                "link": link,
                "date": formatted_date,
                "content": content,
                "keywords": matched_keywords,
                "source": "World Bank",
                "region": "CentralAsia",
                "sector": "sovereigns",
            }
            save_article(artricle_data)
            articles.append(artricle_data)
    return articles

def wb_kaz():
    url = "https://search.worldbank.org/api/v2/news?format=json&rows=20&fct=displayconttype_exact,topic_exact,lang_exact,count_exact,countcode_exact,admreg_exact&src=cq55&apilang=en&lang_exact=English&count_exact=Kazakhstan&os=0"

    payload = {}
    headers = {
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'en-US,en;q=0.9',
      'content-length': '0',
      'content-type': 'text/plain',
      'origin': 'https://www.worldbank.org',
      'priority': 'u=1, i',
      'referer': 'https://www.worldbank.org/',
      'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      'Cookie': '__cf_bm=aPH37XQ4NoLNn_UmzVcUKfHtviVwrA.Sta0x1ouy_qw-1732788147-1.0.1.1-.cjUaqE4nydJYE7sULmfNZVkmQHERph2vTNuJv.UxDJ7K3_jTR33yqDkDK2VpyY4qM3nBPoRNBMqYCP_c4e1vg; search.worldbank.org=4649dbe96dd468ec6356e8c1410cda31; search.worldbank.orgCORS=4649dbe96dd468ec6356e8c1410cda31'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    elements = data.get("documents").values()
    articles = []
    for element in elements:
        title_tag = element.get("title")
        if title_tag is not None:
            title = title_tag.get("cdata!")

        link = element.get("url")

        date = element.get("lnchdt")
        if date is not None:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")


        content_tag = element.get("content")
        if content_tag is not None:
            content = content_tag.get("cdata!")
        matched_keywords = is_ca_related(title, content, sovereign_keywords)
        if not matched_keywords and link is None:
            continue
        if link and link.strip():
            artricle_data = {
                "title": title,
                "link": link,
                "date": formatted_date,
                "content": content,
                "keywords": matched_keywords,
                "source": "World Bank",
                "region": "CentralAsia",
                "sector": "sovereigns",
            }
            save_article(artricle_data)
            articles.append(artricle_data)
    return articles

def wb_arm():
    url = "https://search.worldbank.org/api/v2/news?format=json&rows=20&fct=displayconttype_exact,topic_exact,lang_exact,count_exact,countcode_exact,admreg_exact&src=cq55&apilang=en&lang_exact=English&count_exact=Armenia&os=0"

    payload = {}
    headers = {
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'en-US,en;q=0.9',
      'content-length': '0',
      'content-type': 'text/plain',
      'origin': 'https://www.worldbank.org',
      'priority': 'u=1, i',
      'referer': 'https://www.worldbank.org/',
      'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      'Cookie': '__cf_bm=aPH37XQ4NoLNn_UmzVcUKfHtviVwrA.Sta0x1ouy_qw-1732788147-1.0.1.1-.cjUaqE4nydJYE7sULmfNZVkmQHERph2vTNuJv.UxDJ7K3_jTR33yqDkDK2VpyY4qM3nBPoRNBMqYCP_c4e1vg; search.worldbank.org=4649dbe96dd468ec6356e8c1410cda31; search.worldbank.orgCORS=4649dbe96dd468ec6356e8c1410cda31'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    elements = data.get("documents").values()
    articles = []
    for element in elements:
        title_tag = element.get("title")
        if title_tag is not None:
            title = title_tag.get("cdata!")

        link = element.get("url")

        date = element.get("lnchdt")
        if date is not None:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")


        content_tag = element.get("content")
        if content_tag is not None:
            content = content_tag.get("cdata!")
        matched_keywords = is_ca_related(title, content, sovereign_keywords)
        if not matched_keywords and link is None:
            continue
        if link and link.strip():
            artricle_data = {
                "title": title,
                "link": link,
                "date": formatted_date,
                "content": content,
                "keywords": matched_keywords,
                "source": "World Bank",
                "region": "CentralAsia",
                "sector": "sovereigns",
            }
            save_article(artricle_data)
            articles.append(artricle_data)
    return articles

def wb_aze():
    url = "https://search.worldbank.org/api/v2/news?format=json&rows=20&fct=displayconttype_exact,topic_exact,lang_exact,count_exact,countcode_exact,admreg_exact&src=cq55&apilang=en&lang_exact=English&count_exact=Azerbaijan&os=0"

    payload = {}
    headers = {
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'en-US,en;q=0.9',
      'content-length': '0',
      'content-type': 'text/plain',
      'origin': 'https://www.worldbank.org',
      'priority': 'u=1, i',
      'referer': 'https://www.worldbank.org/',
      'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      'Cookie': '__cf_bm=aPH37XQ4NoLNn_UmzVcUKfHtviVwrA.Sta0x1ouy_qw-1732788147-1.0.1.1-.cjUaqE4nydJYE7sULmfNZVkmQHERph2vTNuJv.UxDJ7K3_jTR33yqDkDK2VpyY4qM3nBPoRNBMqYCP_c4e1vg; search.worldbank.org=4649dbe96dd468ec6356e8c1410cda31; search.worldbank.orgCORS=4649dbe96dd468ec6356e8c1410cda31'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    elements = data.get("documents").values()
    articles = []
    for element in elements:
        title_tag = element.get("title")
        if title_tag is not None:
            title = title_tag.get("cdata!")

        link = element.get("url")

        date = element.get("lnchdt")
        if date is not None:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")


        content_tag = element.get("content")
        if content_tag is not None:
            content = content_tag.get("cdata!")
        matched_keywords = is_ca_related(title, content, sovereign_keywords)
        if not matched_keywords:
            continue


        if link and link.strip():
            artricle_data = {
                "title": title,
                "link": link,
                "date": formatted_date,
                "content": content,
                "keywords": matched_keywords,
                "source": "World Bank",
                "region": "CentralAsia",
                "sector": "sovereigns",
            }
            save_article(artricle_data)
            articles.append(artricle_data)
    return articles

def ca_sov_worldbank():
    articles = wb_uzb() + wb_kaz() + wb_arm() + wb_aze() + wb_aze()
    return articles