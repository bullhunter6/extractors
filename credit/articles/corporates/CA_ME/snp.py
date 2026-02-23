import json
import requests
from langdetect import detect
from utils.check import filter_articles_by_region_2
from utils.db import save_article

COMMON_KEYWORDS = [
    "Fitch Ratings","Moody's", "credit rating", "credit rating agency", "rating methodology",
    "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "credit rating scale",
    "investment grade", "speculative grade", "debt rating", "credit rating model", "credit rating criteria",
    "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review", "bond issuance",
    "sovereign bonds", "M&A", "credit risk", "assigns", "withdraws", "affirms", "upgrades", "downgrades", "guarantee", "guaranty", "guaranteed", "secured", "unsecured",

    "privatisation","corporate rating", "corporate bonds", "standalone credit profile", "issuer default rating", 
    "recovery rating", "recovery percentage", "government related entity", "corporate family rating",
]
 
MIDDLEEAST_COUNTRY_KEYWORDS = ["UAE", "United Arab Emirates", "Saudi Arabia", "GCC countries", "GCC", "Kuwait", "Oman", "Bahrein", "Qatar", "Dubai", "Abu Dhabi","KSA", "saudi", "Middle east", "RAK","Sharjah", "Ras Al Khamiah","Gulf Cooperation Council",
                               "Persian Gulf", "Islamic Cooperation", "Arab League","Muscat","Red Sea", "Yemen", "Jordan", "MENA", "Organization of the Petroleum Exporting Countries", "Arabic Gulf", "Arabian Sea"]

CENTRALASIA_COUNTRY_KEYWORDS = ["Uzbekistan","Kazakh", "Kazakhstan", "Asia and Pacific", "Central Asia","Azerbaijan","Armenia","Turkmenistan","Kyrgyzstan","Tajikistan","Silk Road","Caspian Sea","Eurasia", "Post-Soviet States","Tashkent","Almaty",
                                "Samarkand","Economic Cooperation Organization","Silk Route","OPEC",]
 
MIDDLEEAST_RARE_KEYWORDS = [
    "sukuk",
                            
    "Abu Dhabi National Energy Company", "TAQA", "National Central Cooling", 
    "Vista Global Holding", "ABU DHABI FUTURE ENERGY COMPANY", "Masdar", "DP WORLD", "Shelf Drilling Holdings", 
    "Fertiglobe", "Abu Dhabi Ports Company", "AD Ports Group", "Senaat", "EQUATE Sukuk", "Kuwait Projects", 
    "Damac", "Emaar", "Emirates Telecommunications Group Company", "Etisalat", "Aldar", "ADNOC", "Mamoura", 
    "Abu Dhabi Developmental Holding Company", "DUBAI AEROSPACE ENTERPRISE", "Majid Al Futtaim", "ACWA", 
    "EMIRATES SEMB CORP WATER AND POWER COMPANY", "EWEC", "Oztel", "RUWAIS", "SWEIHAN", "Abu Dhabi Crude Oil Pipeline", 
    "ADCOP", "Dae Funding", "Five Holdings", "Dubai Electricity and Water Authority", "DEWA", "Arada Developments", 
    "Ittihad International Investment", "DIFC Investments", "Emirates Strategic Investment Company", 
    "Private Department", "Taghleef Industries Holdco", "Taghleef Industries Topco", "Vantage Drilling International", 
    "Emirates Airline", "Telford Offshore", "Aerotranscargo FZE", "Brooge Petroleum and Gas Investment Company FZC", 
    "Telford Finco", "ACWA Power Capital Management", "2Rivers DMCC", "Eros Media World", "MRV Holding", 
    "Habtoor International", "A D N H Catering", "Abu Dhabi Aviation", "Abu Dhabi National for Building Materials", 
    "Abu Dhabi National Hotels", "Abu Dhabi National Oil Company For Distribution", "Abu Dhabi Ship Building", 
    "ADNOC Drilling Company", "ADNOC Gas", "ADNOC Logistics & Services", "Agility Global", "Agthia Group", 
    "Air Arabia", "AL KHALEEJ Investment", "Al Seer Marine Supplies & Equipment Company", "Alef Education Holding", 
    "Alpha Dhabi Holding", "Americana Restaurants International", "APEX INVESTMENT", "Aram Group", "Aramex", 
    "Borouge", "BURJEEL HOLDINGS", "Dana Gas", "Depa", "Deyaar Development", "Drake & Scull International", 
    "Dubai Investments", "Dubai Taxi Company", "E7 Group", "Easy Lease Motorcycle Rental", "Emaar Development", 
    "Emirates Central Cooling Systems Corporation", "Emirates Driving Company", "Emirates Integrated Telecommunications Company", 
    "Emirates Reem Investments", "EMSTEEL BUILDING MATERIALS", "ESG EMIRATES STALLIONS GROUP", "ESHRAQ INVESTMENTS", 
    "FOODCO NATIONAL FOODSTUFF", "Fujairah Building Industries", "Fujairah Cement Industries", "Ghitha Holding", 
    "Gulf Cement Co", "Gulf Medical Projects Company", "Gulf Navigation Holding", "Gulf Pharmaceutical Industries", 
    "HILY HOLDING", "International Holding Company", "Manazel", "MBME GROUP", "Modon Holding", "National Cement Co", 
    "National Corporation for Tourism & Hotels", "NATIONAL MARINE DREDGING COMPANY", "NMDC Energy", "Orascom Construction", 
    "PALMS SPORTS", "Parkin Company", "PHOENIX GROUP", "Presight AI Holding", "Pure Health Holding", "RAK Ceramics", 
    "RAK Properties", "Ras Al Khaimah Co for White Cement & Construction Materials", "Salik Company", 
    "Sharjah Cement and Industrial Development Company", "SPACE42", "Spinneys 1961 Holding", "Taaleem Holdings", 
    "Tecom Group", "Union Properties"
    ]

CENTERALASIA_RARE_KEYWORDS = [#removed ADB
    "Uzbek geological exploration", "Uzbek geological", "Chimpharm", "Altynalmas",

    "Navoi Mining and Metallurgical", "Navoi Mining and Metallurgy", "Navoiyuran", 
    "Almalyk Mining and Metallurgical", "Almalyk Mining and Metallurgy", "Almalyk MMC", 
    "Uzbek Metallurgical", "Uzbek Metallurgy", "Uzmetkombinat", "Uzbekneftegaz", "Uztransgaz", 
    "Hududgazta'minot", "Hududgaz", "UzGasTrade", "National Electric Grid of Uzbekistan", 
    "National Electric Grids of Uzbekistan", "Thermal Power Plants", "Regional Electrical Power Networks", 
    "Uzbekgeofizika", "Uzkimyosanoat", "Navoiyazot", "Navoi-Azot", "Navoiazot", 
    "Uzbek Railways", "Oʻzbekiston temir yoʻllari", "O'zbekiston Temir Yollari", 
    "Uzbekiston Temir Yollari", "Ozbekiston Temir Yollari", "Uzbekistan Railways", 
    "Uzbekistan Airways", "Uzbekistan Airports", "Toshshahartransxizmat", "UzAuto", 
    "Uz Auto", "Uzautosanoat", "Uzauto-sanoat", "Uzbektelecom", "Uzbek telecom", 
    "Uztelecom", "O'zbekiston pochtasi", "UzPost", "Uzbekistan Post", "Uzbekcoal", 
    "Artel Electronics", "Dehkanabad Potash Plant", "Dekhkanabad plant of potassium", 
    "Toshkent Metallurgiya Zavodi", "Tashkent Metallurgical Plant", "Tashkent Metallurgy Plant", 
    "SamAuto", "Samarqand Avtomobil zavodi", "SamAvto", "Akfa Aluminium", "Enter Engineering", 
    "Saneg", "Sanoat Energetika Guruhi", "Fargonaazot", "Farg'onaazot", "Hududiy Elektr Tarmoqla", 
    "Uzsungwoo", "QuvasoyCement", "Quvasoy Cement", "Kuvasaycement", "POSCO International Textile", 
    "Promxim Impex", "Kazakhstan Housing Company", "Samruk-Energy", "Samruk-Energo", 
    "Samruk Energy", "Samruk Energo", "Ekibastuz GRES-1", "Ekibastuz GRES 1", 
    "Samruk-Kazyna Construction", "Samruk Kazyna Construction", "Kazpost", "QazPost", 
    "Kazakhtelecom", "Kcell", "Kazakhstan Electricity Grid Operating Company", "KEGOC", 
    "KazMunayGas", "KazTransOil", "Astana Gas", "Astanagas", "Astana-Gas", "QazaqGaz", 
    "Intergas Central Asia", "KazTransGas", "Kazatomprom", "Kazakhstan Temir Zholy", 
    "Qazaqstan Temır Joly", "Kaztemirtrans", "Tengizchevroil", "Eurasian Resources Group", 
    "BI Group", "Kazakhstan Utility Systems", "Mangistau Regional Electricity Network", 
    "Food Contract Corp", "Food Contract Corporation", "TransteleCom", "Kaz Minerals", 
    "Kazakhmys", "BI Development", "Alma Telecommunications", "Batys transit", 
    "KazMunaiGas", "Kaztemirtrans", "Integra Construction"]

REGIONAL_KEYWORDS = {
    "MiddleEast": MIDDLEEAST_COUNTRY_KEYWORDS,
    "CentralAsia": CENTRALASIA_COUNTRY_KEYWORDS,
}

RARE_KEYWORDS = {
    "MiddleEast": MIDDLEEAST_RARE_KEYWORDS,
    "CentralAsia": CENTERALASIA_RARE_KEYWORDS,
}

def translate_text(text, source_lang, target_lang="en"):
    url = "https://translate-pa.googleapis.com/v1/translateHtml"
    headers = {
        'accept': '*/*',
        'content-type': 'application/json+protobuf',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-goog-api-key': 'AIzaSyATBXajvzQLTDHEQbcpq0Ihe0vWDHmO520'
    }
    payload = json.dumps([
        [text, source_lang, target_lang],
        "te_lib"
    ])

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        try:
            return response.json()[0][0]
        except (IndexError, KeyError):
            print("Error parsing translation response.")
            return text
    else:
        print(f"Translation failed with status code {response.status_code}")
        return text

def snp_cp():
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
                    #detected_lang_title = detect(title)
                #if detected_lang_title != "en":
                    #trans_title = translate_text(title, detected_lang_title)
                #detected_lang_content = detect(content)
                #if detected_lang_content != "en":
                    #trans_content = translate_text(content, detected_lang_content)

                region, keywords = filter_articles_by_region_2(title, content, COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS)
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
                        "sector": "corporates"
                    })
                    save_article(articles_info)
                    articles.append(articles_info)

    return articles

