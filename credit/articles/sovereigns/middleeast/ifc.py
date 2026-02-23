import json
import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime
import re
from utils.db import save_article
from utils.check import me_related
from utils.keywords import me_ifc_KEYWORDS

logging.basicConfig(level=logging.INFO)

sovereign_keywords =[
    "sovereign","sovereign rating","UAE", "United Arab Emirates", "Saudi Arabia", "GCC countries", "GCC", "Kuwait", "Oman", "Bahrein", "Qatar", "Dubai", "Abu Dhabi","KSA", "saudi", 
    "Middle east", "RAK","Sharjah", "Ras Al Khamiah","Gulf Cooperation Council","Persian Gulf", "Islamic Cooperation", "Arab League","Muscat","Red Sea", "Yemen", "Jordan", 
    "MENA", "OPEC", "Organization of the Petroleum Exporting Countries", "Arabic Gulf", "Arabian Sea",
    
    "key initiatives","sanctions","Finance system","local goverment","goverment","goverment bonds","goverment spending","goverment budget",
    "goverment deficit","goverment surplus","goverment revenue","goverment expenditure","goverment fiscal policy","goverment monetary policy","goverment stimulus","goverment recovery",
    "goverment growth","goverment outlook","goverment impact","goverment contraction","goverment indicators","goverment rate cut","goverment mortgage","goverment mortgages",
    "goverment interest rate","goverment interest rates","goverment central bank","goverment central banks","goverment monetary policy","goverment fiscal policy",
    "goverment budget","goverment budgets","goverment deficit","goverment deficits","goverment government debt","goverment debt to GDP","goverment GDP","goverment GDP growth",
    "goverment economy","goverment economic","goverment economic growth","goverment economic outlook","goverment economic recovery","goverment economic stimulus",
    "goverment economic stimulus package","goverment economic impact","goverment economic contraction","goverment economic indicators","goverment rate cut",
    "goverment mortgage","goverment mortgages",'interest rate','interest rates','monetary policy','fiscal policy','goverment budget','goverment budgets','deficit',
    'deficits','government debt','debt to GDP','GDP','GDP growth',"economic growth","economic outlook","economic recovery","economic stimulus",
    "economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgage","mortgages","sukuk","economic growth","economic outlook",
    "economic recovery","economic stimulus","economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgage","mortgages",'inflation'
]   

def ifc_uae():
    url = "https://webapi.worldbank.org/aemsite/ifc/search"

    payload = json.dumps({
      "search": "*",
      "facets": [
        "contentDate,sort:value,count:10000",
        "language,sort:value,count:10000",
        "countries,sort:value,count:10000",
        "topics,sort:value,count:10000",
        "regions,sort:value,count:10000",
        "subTopics,sort:value,count:10000",
        "contentType,sort:value,count:10000"
      ],
      "filter": "(countries/any(countries: countries eq 'United Arab Emirates')) and (language eq 'English') and (contentType eq 'Press Release') ",
      "count": True,
      "top": 20,
      "skip": 0,
      "orderby": "contentDate desc",
      "highlight": "title-1,bodyContent-1",
      "highlightPostTag": "</span>",
      "highlightPreTag": "<span class='ppfhighlight'>",
      "searchFields": "title"
    })
    headers = {
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/json',
      'ocp-apim-subscription-key': 'a02440fa123c4740a83ed288591eafe4',
      'origin': 'https://www.ifc.org',
      'priority': 'u=1, i',
      'referer': 'https://www.ifc.org/',
      'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'cross-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      'Cookie': '__cf_bm=lUkqvK529fmBJtNsta3XnOnzXFHFhcYji4XvSZIHZp0-1732716000-1.0.1.1-EcqkL8nYtBJPVLj.GHBoP1SHIYXvEar3BbkSkwc2uJQyaYs9OHwOZntFQWbzStNicR6On1HO.Zh2H5LN9tR62Q; webapi.worldbank.org=0c8444a98c4582b339c96fb7a19d95f9; webapi.worldbank.orgCORS=0c8444a98c4582b339c96fb7a19d95f9'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    articles = []
    elements = data.get("value")
    for element in elements:
        title = element.get("title")
        link = element.get("pagePublishPath")
        full_link = f"https://www.ifc.org{link}"
        published_date = element.get("contentDate")
        formatted_date = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")

        content_response = requests.request("GET", full_link)
        content_soup = BeautifulSoup(content_response.text, 'html.parser')
        divs = content_soup.find_all("div",class_="container responsivegrid aem-GridColumn--default--none aem-GridColumn--offset--desktop--2 aem-GridColumn--offset--default--2 aem-GridColumn--offset--phone--0 aem-GridColumn--desktop--none aem-GridColumn--tablet--10 aem-GridColumn--desktop--8 aem-GridColumn--phone--none aem-GridColumn--phone--12 aem-GridColumn--tablet--none aem-GridColumn aem-GridColumn--default--8 aem-GridColumn--offset--tablet--1")
        for div in divs:
            content = div.get_text(strip=True)
        matched_keywords = me_related(title, content, sovereign_keywords)
        if not matched_keywords:
            logging.debug(f"Skipping non-relevant article: {title}")
            continue
        article_info = ({
            "title": title,
            "link": full_link,
            "date": formatted_date,
            "content": content,
            "keywords": matched_keywords,
            "source": "IFC",
            "region": "MiddleEast",
            "sector": "sovereigns"
        })
        save_article(article_info)
        articles.append(article_info)
    return articles

def ifc_sau():
    url = "https://webapi.worldbank.org/aemsite/ifc/search"

    payload = json.dumps({
      "search": "*",
      "facets": [
        "contentDate,sort:value,count:10000",
        "language,sort:value,count:10000",
        "countries,sort:value,count:10000",
        "topics,sort:value,count:10000",
        "regions,sort:value,count:10000",
        "subTopics,sort:value,count:10000",
        "contentType,sort:value,count:10000"
      ],
      "filter": "(countries/any(countries: countries eq 'Saudi Arabia')) and (language eq 'English') and (contentType eq 'Press Release') ",
      "count": True,
      "top": 20,
      "skip": 0,
      "orderby": "contentDate desc",
      "highlight": "title-1,bodyContent-1",
      "highlightPostTag": "</span>",
      "highlightPreTag": "<span class='ppfhighlight'>",
      "searchFields": "title"
    })
    headers = {
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/json',
      'ocp-apim-subscription-key': 'a02440fa123c4740a83ed288591eafe4',
      'origin': 'https://www.ifc.org',
      'priority': 'u=1, i',
      'referer': 'https://www.ifc.org/',
      'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'cross-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      'Cookie': '__cf_bm=vCIMoiYfdJsO0qSdlinBDIFaHLAf9I6d1HENBT5Jslo-1732718618-1.0.1.1-Bg4_KTHh8SZCuXoVKHDzWaC18UCP1v2tsY_OXi2bDf0oto3wRvqkd9OlvRlDlEl3ki.pfAGyS_Chs35el3R4TA; webapi.worldbank.org=0c8444a98c4582b339c96fb7a19d95f9; webapi.worldbank.orgCORS=0c8444a98c4582b339c96fb7a19d95f9'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    elements = data.get("value")
    articles = []
    for element in elements:
        title = element.get("title")
        link = element.get("pagePublishPath")
        full_link = f"https://www.ifc.org{link}"
        published_date = element.get("contentDate")
        formatted_date = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")

        content_response = requests.request("GET", full_link)
        content_soup = BeautifulSoup(content_response.text, 'html.parser')
        divs = content_soup.find_all("div",class_="container responsivegrid aem-GridColumn--default--none aem-GridColumn--offset--desktop--2 aem-GridColumn--offset--default--2 aem-GridColumn--offset--phone--0 aem-GridColumn--desktop--none aem-GridColumn--tablet--10 aem-GridColumn--desktop--8 aem-GridColumn--phone--none aem-GridColumn--phone--12 aem-GridColumn--tablet--none aem-GridColumn aem-GridColumn--default--8 aem-GridColumn--offset--tablet--1")
        for div in divs:
            content = div.get_text(strip=True)
        matched_keywords = me_related(title, content, sovereign_keywords)
        if not matched_keywords:
            continue
        article_info = ({
            "title": title,
            "link": full_link,
            "date": formatted_date,
            "content": content,
            "keywords": matched_keywords,
            "source": "IFC",
            "region": "MiddleEast",
            "sector": "sovereigns"
        })
        save_article(article_info)
        articles.append(article_info)
    return articles


def sov_me_ifc():
    articles = ifc_uae() + ifc_sau()
    return articles