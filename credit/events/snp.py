import requests
from bs4 import BeautifulSoup
from utils.db import save_events

def get_location(url):
    headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-US,en;q=0.9',
      'cache-control': 'max-age=0',
      'cookie': 'captcha-image-209796=NUxnpTyRD2iNNV7FUAFaDQ==; bc_tstgrp=17; s_inv=0; opvc=eb35eb32-34c7-4ec3-94f8-9f2bfb5cfd5e; sitevisitscookie=1; dmid=f463d617-41b8-4adf-a9f0-ae975390d299; AMCVS_92221CFE533057500A490D45%40AdobeOrg=1; AMCV_92221CFE533057500A490D45%40AdobeOrg=179643557%7CMCIDTS%7C19843%7CMCMID%7C03701438445244117284460734832984461550%7CMCOPTOUT-1714376610s%7CNONE%7CvVersion%7C5.5.0; last_visit_bc=1714631808947; _zitok=377c35becc1c6bc525d91715583012; captcha-image-857636=ImPI00Ig+axXBLyVQ9WPIg==; marketintelligence-brand-campaign=Ad_Type_Medium__c=cpc&Ad_Source__c=&Ad_Campaign__c=Brand_ESG_Search&Ad_Content__c=534418150272&Ad_Term_s__c=&AdWords_Campaign_Name__c=&AdWords_ID__c=&AdWords_Keyword__c=&full_ref_url=unknown; _cq_duid=1.1719386881.yBiFbzwf2ogTjPBg; _cq_suid=1.1719386881.HZZFI0qVNdBB2CDv; ASP.NET_SessionId=jxnvupu24yl4bq3fxztuh0me; driftt_aid=7ce0118a-b0a0-4202-bbd5-a9a67ae08d9f; drift_aid=7ce0118a-b0a0-4202-bbd5-a9a67ae08d9f; JSESSIONID=D74A60423CF8389BBF14F679D97F4C26.10.58.59.41; SNLStack=STACK1; OptanonAlertBoxClosed=2025-01-14T09:01:24.833Z; TRINITY_USER_DATA=eyJ1c2VySWRUUyI6MTczNjg0NjcyNzcyM30=; TRINITY_USER_ID=46f712c4-26eb-48b7-a7aa-97cabb614611; BNI_persistence=UeLbLrl1461xKZfyh1owx08wu-dxEHMOlnEKf9YF0tJa6jjkQ-juJum7RxvMF3dKDqOWwzI8A7gXhP9x0YhzCw==; AWSALB=6xCt4JmaGiGosnJrt6K/WHPA0htvcLKxgLSdWbMSr5dGw7rxMjEVPPxhiNWBtbTYpFBwSF96Ljobed6I8KJ3kLpn6o6KFwgG7VvHwh489kNewxR/7sasDTSQc5UT; AWSALBCORS=6xCt4JmaGiGosnJrt6K/WHPA0htvcLKxgLSdWbMSr5dGw7rxMjEVPPxhiNWBtbTYpFBwSF96Ljobed6I8KJ3kLpn6o6KFwgG7VvHwh489kNewxR/7sasDTSQc5UT; search-token-test=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZWFyY2gtcXVlcnkiLCJjbGllbnQtaWQiOiJ3ZWItc2VhcmNoIiwiZXhwIjoxNzM3MTAwNjU3MjQ0fQ.fdLvXV6PW5SLLa8_J7z8nDunYpEtbRlGsLQnJ7ezZSQ; search-token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZWFyY2gtcXVlcnkiLCJjbGllbnQtaWQiOiJ3ZWItc2VhcmNoIiwiZXhwIjoxNzM3MTAwNjU3MjQ0fQ.fdLvXV6PW5SLLa8_J7z8nDunYpEtbRlGsLQnJ7ezZSQ; s_dur=1737099560335; session_start_timestamp=1737099619; drift_campaign_refresh=9afc84cd-3056-4626-827b-e15230fa8c4b; s_gpv=www.spglobal.com:ratings:en:events:hosted-events:2025-vietnam-credit-spotlight-feb-27-2025-; s_nr365=1737099623282-Repeat; s_tslv=1737099623284; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jan+17+2025+11%3A40%3A23+GMT%2B0400+(Gulf+Standard+Time)&version=202409.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=689de3b6-3204-42eb-b287-ab7b79be6472&interactionCount=2&isAnonUser=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0004%3A1%2CC0002%3A1%2CC0001%3A1&AwaitingReconsent=false&intType=1&geolocation=AE%3BDU',
      'priority': 'u=0, i',
      'referer': 'https://www.spglobal.com/en/search',
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

    soup = BeautifulSoup(response.text, 'html.parser')
    location_row = soup.find_all("div", class_="filterable-list__row")[1] if len(soup.find_all("div", class_="filterable-list__row")) > 1 else None
    if location_row:
        location_spans = location_row.find_all("span")
        location = location_spans[-1].text.strip() if location_spans else "N/A"
    else:
        location = "N/A"
    return location

def snp_events():
    url = "https://www.spglobal.com/api/apps/spglobal-prod/query/spglobal-prod?q=*%3A*&rows=100&pagenum=1&fq=es_content_type_s:(%22Events%22)&cfl=es_unified_dt,es_primary_image_url_s,es_division_s,es_content_type_s,es_author_thumbnails_ss,es_authors_ss,es_author_url_ss&division=corporate"
    url2= "https://www.spglobal.com/api/apps/spglobal-prod/query/spglobal-prod?q=*%3A*&rows=20&pagenum=1&sort=es_event_start_date_dt%20asc&fq=es_event_end_date_dt:%5B2025-10-29T11%3A11%3A09.064Z%20TO%20*%5D&fq=es_content_type_s:(%22Events%22OR%22Awards%22OR%22Briefing%22OR%22Conferences%22OR%22Forums%22OR%22Methodology%20Education%22OR%22Seminars%22OR%22Training%22OR%22eLearning%22OR%22Webinar%20Replays%22OR%22Webinar%22OR%22Market%20Briefing%22OR%22Benchmark%20Briefing%22)&fq=es_division_s:(%22S%26P%20Global%20Commodity%20Insights%22)&cfl=es_event_start_date_dt,es_primary_image_url_s,es_event_category_s,es_author_thumbnails_ss,es_authors_ss,es_author_url_ss,es_event_subcontenttype_ss&tags=ci_event_list&division=commodity-insights"
    payload = {}
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZWFyY2gtcXVlcnkiLCJjbGllbnQtaWQiOiJ3ZWItc2VhcmNoIiwiZXhwIjoxNzM3MTAwNjU3MjQ0fQ.fdLvXV6PW5SLLa8_J7z8nDunYpEtbRlGsLQnJ7ezZSQ',
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

    response = requests.get(url, headers=headers, data=payload)
    events = []
    if response.status_code == 200:
        data = response.json()
        elements = data.get('response', {})
        docs = elements.get('docs', [])
        for doc in docs:
            title = doc.get('es_title_t', 'N/A')
            date = doc.get('es_unified_dt', 'N/A')
            link = doc.get('es_url_s', '')

            if link.startswith("http"):
                full_link = link
            elif link.startswith("/"):
                full_link = f"https://www.spglobal.com{link}"
            else:
                full_link = "N/A"

            location = get_location(full_link) if full_link != "N/A" else "N/A"

            events.append({
                "title": title,
                "date": date,
                "link": full_link,
                "source": "S&P Global",
                "location": location,
                "details": "N/A"
            })
            save_events(events, source="S&P Global")


    return events


