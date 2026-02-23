import requests
from utils.db import save_article

COMMON_KEYWORDS = [#use these keywords + country keywords, no rare keywords
    "Fitch Ratings","Moody's", "credit rating agency", "rating methodology",
    "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "credit rating scale",
    "investment grade", "speculative grade", "debt rating", "credit rating model", "credit rating criteria",
    "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review","sovereign bonds",
    
    "privatisation","Finance system","local goverment","goverment","goverment bonds","goverment spending","goverment budget",
    "goverment deficit","goverment surplus","goverment revenue","goverment expenditure","goverment fiscal policy","goverment monetary policy","goverment stimulus","goverment recovery",
    "goverment growth","goverment outlook","goverment impact","goverment contraction","goverment indicators","goverment rate cut","goverment mortgage","goverment mortgages",
    "goverment interest rate","goverment interest rates","goverment central bank","goverment central banks","goverment monetary policy","goverment fiscal policy",
    "goverment budget","goverment budgets","goverment deficit","goverment deficits","goverment government debt","goverment debt to GDP","goverment GDP","goverment GDP growth",
    "goverment economy","goverment economic","goverment economic growth","goverment economic outlook","goverment economic recovery","goverment economic stimulus",
    "goverment economic stimulus package","goverment economic impact","goverment economic contraction","goverment economic indicators","goverment rate cut",
    "goverment mortgage","goverment mortgages",'interest rate','interest rates','monetary policy','fiscal policy','goverment budget','goverment budgets',
    'deficits','government debt','debt to GDP','GDP','GDP growth',"economic growth","economic outlook","economic recovery","economic stimulus",
    "economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgage","mortgages","sukuk","economic growth","economic outlook",
    "economic recovery","economic stimulus","economic stimulus package","economic impact","economic contraction","economic indicators","rate cut","mortgage","mortgages",
]

MIDDLEEAST_COUNTRY_KEYWORDS = ["UAE", "United Arab Emirates", "Saudi Arabia", "GCC countries", "GCC", "Kuwait","Bahrein", "Qatar", "Dubai", "Abu Dhabi","KSA", "saudi", "Middle east","Sharjah", "Ras Al Khamiah","Gulf Cooperation Council",
                               "Persian Gulf", "Islamic Cooperation", "Arab League","Muscat","Red Sea", "Yemen", "Jordan", "MENA", "Organization of the Petroleum Exporting Countries", "Arabic Gulf", "Arabian Sea"]

CENTRALASIA_COUNTRY_KEYWORDS = ["Uzbekistan","Kazakh", "Kazakhstan", "Asia and Pacific", "Central Asia","Azerbaijan","Armenia","Turkmenistan","Kyrgyzstan","Tajikistan","Silk Road","Caspian Sea","Eurasia", "Post-Soviet States","Tashkent","Almaty",
                                "Samarkand","Economic Cooperation Organization","Silk Route", "OPEC"]


REGIONAL_KEYWORDS = {
    "MiddleEast": MIDDLEEAST_COUNTRY_KEYWORDS,
    "CentralAsia": CENTRALASIA_COUNTRY_KEYWORDS,
}

def filter_articles(title, content, common_keywords, regional_keywords):
    matched_common_keywords = [kw for kw in common_keywords if kw.lower() in (title + content).lower()]

    for region, country_keywords in regional_keywords.items():
        matched_country_keywords = [kw for kw in country_keywords if kw.lower() in (title + content).lower()]
        if matched_common_keywords and matched_country_keywords:
            matched_keywords = matched_common_keywords + matched_country_keywords
            return region, matched_keywords
    return None, None


def snp_sov():
    url = "https://www.spglobal.com/api/apps/spglobal-prod/query/spglobal-prod?q=*%3A*&rows=300&pagenum=1&sort=es_unified_dt%20desc&fq=es_content_type_s:(%22Articles%22OR%22Blog%22OR%22Corrections%22OR%22Expert%20Bio%22OR%22Indices%20Research%22OR%22Market%20Intelligence%20Research%22OR%22News%22OR%22PDF%20Details%22OR%22Podcast%22OR%22Press%20Releases%22OR%22Products%22OR%22Subscriber%20Notes%22OR%22Symbols%22OR%22Video%22)&division=corporate"

    payload = {}
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZWFyY2gtcXVlcnkiLCJjbGllbnQtaWQiOiJ3ZWItc2VhcmNoIiwiZXhwIjoxNzM2ODQ3OTMxMTQzfQ.x-N-tU63LOI_wu4Ze5GTH5f5U3jbmiLb2GHxFqimSzI',
    'cookie': 'captcha-image-209796=NUxnpTyRD2iNNV7FUAFaDQ==; bc_tstgrp=17; s_inv=0; opvc=eb35eb32-34c7-4ec3-94f8-9f2bfb5cfd5e; sitevisitscookie=1; dmid=f463d617-41b8-4adf-a9f0-ae975390d299; AMCVS_92221CFE533057500A490D45%40AdobeOrg=1; AMCV_92221CFE533057500A490D45%40AdobeOrg=179643557%7CMCIDTS%7C19843%7CMCMID%7C03701438445244117284460734832984461550%7CMCOPTOUT-1714376610s%7CNONE%7CvVersion%7C5.5.0; last_visit_bc=1714631808947; _zitok=377c35becc1c6bc525d91715583012; captcha-image-857636=ImPI00Ig+axXBLyVQ9WPIg==; marketintelligence-brand-campaign=Ad_Type_Medium__c=cpc&Ad_Source__c=&Ad_Campaign__c=Brand_ESG_Search&Ad_Content__c=534418150272&Ad_Term_s__c=&AdWords_Campaign_Name__c=&AdWords_ID__c=&AdWords_Keyword__c=&full_ref_url=unknown; _cq_duid=1.1719386881.yBiFbzwf2ogTjPBg; _cq_suid=1.1719386881.HZZFI0qVNdBB2CDv; ASP.NET_SessionId=jxnvupu24yl4bq3fxztuh0me; driftt_aid=7ce0118a-b0a0-4202-bbd5-a9a67ae08d9f; drift_aid=7ce0118a-b0a0-4202-bbd5-a9a67ae08d9f; JSESSIONID=D74A60423CF8389BBF14F679D97F4C26.10.58.59.41; SNLStack=STACK1; OptanonAlertBoxClosed=2025-01-14T09:01:24.833Z; session_start_timestamp=1736846699; s_gpv=www.spglobal.com:ratings:en:research:articles:250113-great-capexpectations-tech-utility-spending-power-capital-goods-revenue-growth-in-2025-13381132; count=1|Tue, 14 Jan 2025 17:25:26 GMT; TRINITY_USER_DATA=eyJ1c2VySWRUUyI6MTczNjg0NjcyNzcyM30=; TRINITY_USER_ID=46f712c4-26eb-48b7-a7aa-97cabb614611; search-token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZWFyY2gtcXVlcnkiLCJjbGllbnQtaWQiOiJ3ZWItc2VhcmNoIiwiZXhwIjoxNzM2ODQ3OTMxMTQzfQ.x-N-tU63LOI_wu4Ze5GTH5f5U3jbmiLb2GHxFqimSzI; s_dur=1736846861368; AWSALB=eaU92r/zscpT2AP2OrAfUqFoqKBwUHWxx9kDNZC5R7BH/bfwzGoBV/aQzDHZdwKz79y8EO2ZCBt2YoQaa23dil2ci0Fw/nX0YmMZTUmAR74B6ysQU+RLLjpUgCRy; AWSALBCORS=eaU92r/zscpT2AP2OrAfUqFoqKBwUHWxx9kDNZC5R7BH/bfwzGoBV/aQzDHZdwKz79y8EO2ZCBt2YoQaa23dil2ci0Fw/nX0YmMZTUmAR74B6ysQU+RLLjpUgCRy; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jan+14+2025+13%3A29%3A30+GMT%2B0400+(Gulf+Standard+Time)&version=202409.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=689de3b6-3204-42eb-b287-ab7b79be6472&interactionCount=2&isAnonUser=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0004%3A1%2CC0002%3A1%2CC0001%3A1&AwaitingReconsent=false&intType=1&geolocation=AE%3BDU; drift_campaign_refresh=6983f59f-7347-4144-8839-1686357b3b07; s_nr365=1736847057365-Repeat; s_tslv=1736847057366',
    'priority': 'u=1, i',
    'referer': 'https://www.spglobal.com/en/search',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    articles = []
    if response.status_code == 200:
        data = response.json()
        elements = data.get('response', [])
        docs = elements.get('docs', [])
        for doc in docs:
            title = doc.get('es_title_t', '')
            content = doc.get('es_body_content_txt', [])
            date = doc.get('es_unified_dt', '')
            link = doc.get('es_url_s', '')
            full_link = f"https://www.spglobal.com{link}"
            if link.startswith("http"):
                full_link = link
            elif link.startswith("/"):
                full_link = f"https://www.spglobal.com{link}"
            else:
                full_link = "N/A"


            if isinstance(content, list):
                content = ' '.join(content)
            if content:
                region, keywords = filter_articles(title, content, COMMON_KEYWORDS, REGIONAL_KEYWORDS)
                if keywords:
                    if "Daily Update" in title or "Trump" in title:
                        continue
                    articles_info = ({
                        "title": title,
                        "date": date,
                        "link": full_link,
                        "content": content,
                        "region": region,
                        "keywords": keywords,
                        "source": "S&P Global",
                        "sector": "sovereigns"
                    })
                    save_article(articles_info)
                    articles.append(articles_info)

    return articles
