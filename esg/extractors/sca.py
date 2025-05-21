import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
from utils.db_utils import save_article
from utils.check import is_esg_related
import logging

def sca_articles():
    url = "https://www.sca.gov.ae/services/AjaxHandler.asmx/LoadNewsList"
    payload = json.dumps({
        "pageIndex": 1,
        "pageSize": 5,
        "languageId": 1,
        "languageCode": "en-GB",
        "isArchived": False,
        "thumbnailSizeFactor": "4d81x3201wffffff",
        "excludeItems": [26689],
        "keyword": "",
        "categoryId": None,
        "toDate": "",
        "fromDate": ""
    })
    api_headers = {
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'Accept-Language': 'en-US,en;q=0.9',
      'Connection': 'keep-alive',
      'Content-Type': 'application/json; charset=UTF-8',
      'Cookie': 'ASP.NET_SessionId=yowt5tscz4aaqhb5ffnq2w0t; icms_Lang=en-GB; __RequestVerificationToken=aH+E19x/vaWrJ11K0RRm5WvMWLl/g4+W0Ze6LWvSJUo29JeVDa5IMpdX7uyY6GDQnxj6DbGT1GJtLm6tRaPY/A==; Eservices2=!yH3/h+439xI4+1nVxWyohBunzVxXf3Jb1Zbze2/WI2HJXXvlkFe0cEnomhqdg4dovv1qHZLzQEZeeA==; theme=greentheme; __zlcmid=1MtmtC0wqKqOkkV; SameSite=None; ADRUM_BTa=R:48|g:1d082468-0238-45f2-83f7-92a018e56daf|n:SCA_d9cdb7e9-fa27-460d-b79a-1f86b592f158; TS0109f433=01686b6511c346cdffc9534f8ec44a7e061eb199695815d2e15a451630641363f9457ff7d90ecf3ecf826063494e4ee0275272c492de04b8bf01c3b27e792420f1a3ed75885c7a7cffd4a32f8bf4fec39e5009f0e2ed560185dfaa50a528601f4148c25a71d6857fd6e5eb32c264fd299367142e566e441402fd31ffe3a64e4d1b7a2505751aea2d2c10c952d2a1df3fd3453c8b61a45e64ebd5e4df85ab6b9abee5995f480a54734430f7c962cace78c062ad1dec4a4f9bc21669aa7b65623a9f828c0088; TS0109f433=01686b6511e93676b7c4d210ff494b98efd8cba45d993be3c6edd6bb1e75c65fc5c5529a21dd301fcf7b8c3708cfb6af6e526ea8c94d3fc074fa640b25b655a552cd459ebeab079f1571870c899c3a736ce783ecdb3ffeec985be72d3ecfa72d0f550a3f645202051d01356f4c55ec191f6d31c57b9ef6e71981dcc52887ac094a3b097b5f2fab11a6dec5dbf2b23ff272a7d0fc7cb09db04df4e8e7e1d70c5da901c9913a0ed0ae5e8f16da6b92d620f76d3c820f61c3ce5bc31906ce8d98b9bfcd68f7bc',
      'Origin': 'https://www.sca.gov.ae',
      'Referer': 'https://www.sca.gov.ae/en/media-center/news.aspx',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
      'X-Requested-With': 'XMLHttpRequest',
      'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"'
    }
    artilce_headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'Accept-Language': 'en-US,en;q=0.9',
      'Connection': 'keep-alive',
      'Cookie': 'ASP.NET_SessionId=yowt5tscz4aaqhb5ffnq2w0t; icms_Lang=en-GB; __RequestVerificationToken=aH+E19x/vaWrJ11K0RRm5WvMWLl/g4+W0Ze6LWvSJUo29JeVDa5IMpdX7uyY6GDQnxj6DbGT1GJtLm6tRaPY/A==; Eservices2=!yH3/h+439xI4+1nVxWyohBunzVxXf3Jb1Zbze2/WI2HJXXvlkFe0cEnomhqdg4dovv1qHZLzQEZeeA==; theme=greentheme; __zlcmid=1MtmtC0wqKqOkkV; TS0109f433=01686b6511c346cdffc9534f8ec44a7e061eb199695815d2e15a451630641363f9457ff7d90ecf3ecf826063494e4ee0275272c492de04b8bf01c3b27e792420f1a3ed75885c7a7cffd4a32f8bf4fec39e5009f0e2ed560185dfaa50a528601f4148c25a71d6857fd6e5eb32c264fd299367142e566e441402fd31ffe3a64e4d1b7a2505751aea2d2c10c952d2a1df3fd3453c8b61a45e64ebd5e4df85ab6b9abee5995f480a54734430f7c962cace78c062ad1dec4a4f9bc21669aa7b65623a9f828c0088; ADRUM_BT1=R:48|i:48735|e:2078; ADRUM_BTa=R:48|g:4809c48a-2e44-4fa5-90ee-3d90fd3a5ca3|n:SCA_d9cdb7e9-fa27-460d-b79a-1f86b592f158; SameSite=None; TS0109f433=01686b65111acc9298c67f70df2a88bce6fbdcfe29993be3c6edd6bb1e75c65fc5c5529a21dd301fcf7b8c3708cfb6af6e526ea8c94d3fc074fa640b25b655a552cd459ebeab079f1571870c899c3a736ce783ecdb30ee1af3d20d6d4ab0f8c7d4c204d64c5425580aa67dced189d10348a4ebdae0808cb6d9d761f50b7d4d366ad9d19f66899d368449be5671d281eb1e425af3a46d96e8c7eb44dec197702c8bbb472071b85234fc360fd0a13b1f262d84cdaa31e5947f2e10718a581aba71756109a929; icms_Lang=en-GB',
      'Referer': 'https://www.sca.gov.ae/en/media-center/news.aspx',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-User': '?1',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
      'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"'
    }
    response = requests.post(url, headers=api_headers, data=payload)
    response_data = response.json()
    articles = response_data.get("d", {}).get("items", [])
    extracted_articles  = []
    
    for article in articles:
        title = article.get("fullTitle", "No title")
        date_raw = article.get("date", "No date")
        try:
            date_obj = datetime.strptime(date_raw.split(", ")[-1], "%B %d, %Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
        except ValueError:
            formatted_date = "Invalid date format"
        if formatted_date == "Invalid date format":
            try:
                date_obj = datetime.strptime(date_raw, "%A, %B %d, %Y")
                formatted_date = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                formatted_date = "Invalid date format"

        link = "https://" + article.get("fullLink", "No link")
        response = requests.get(link, headers=artilce_headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        content_element = soup.find("div", class_="text")
        paragraphs = content_element.find_all("p") if content_element else []
        article_content = "\n\n".join(p.get_text(strip=True) for p in paragraphs)
        matched_keywords = is_esg_related(title, article_content)
        if not matched_keywords:
            logging.debug(f"Skipping non-relevant article: {title}")

        articles_data = ({
            "title": title,
            "date": formatted_date,
            "url": link,
            "summary": article_content,
            "source": "Securities and Commodities Authority",
            "keywords": matched_keywords
        })
        save_article(articles_data)
        extracted_articles .append(articles_data)
    
    return extracted_articles 