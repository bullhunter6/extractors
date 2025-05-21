import requests
from datetime import datetime
from utils.db_utils import save_events_to_csv

def sp_events():
    url = "https://www.spglobal.com/api/apps/spglobal-prod/query/spglobal-prod?q=*%3A*&rows=33&pagenum=1&sort=es_event_start_date_dt%20asc&fq=es_content_type_s:%22Events%22&fl=es_title_t,es_event_start_date_dt,es_body_content_txt,es_url_s,es_primary_image_url_s,es_event_category_s&fq=es_event_end_date_dt:%5B2024-05-27T06%3A18%3A32.453Z%20TO%20*%5D&tags=default_facets_en"
    payload = {}
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZWFyY2gtcXVlcnkiLCJjbGllbnQtaWQiOiJ3ZWItc2VhcmNoIiwiZXhwIjoxNzM4MTMxNzU0Mzg5fQ.R_ZqqC9d8HEpsMDWRbmiqNXeHiSGxqKGZTfSECKQMCQ',
    'cookie': 'captcha-image-209796=NUxnpTyRD2iNNV7FUAFaDQ==; bc_tstgrp=17; s_inv=0; opvc=eb35eb32-34c7-4ec3-94f8-9f2bfb5cfd5e; sitevisitscookie=1; dmid=f463d617-41b8-4adf-a9f0-ae975390d299; AMCVS_92221CFE533057500A490D45%40AdobeOrg=1; AMCV_92221CFE533057500A490D45%40AdobeOrg=179643557%7CMCIDTS%7C19843%7CMCMID%7C03701438445244117284460734832984461550%7CMCOPTOUT-1714376610s%7CNONE%7CvVersion%7C5.5.0; last_visit_bc=1714631808947; _zitok=377c35becc1c6bc525d91715583012; captcha-image-857636=ImPI00Ig+axXBLyVQ9WPIg==; marketintelligence-brand-campaign=Ad_Type_Medium__c=cpc&Ad_Source__c=&Ad_Campaign__c=Brand_ESG_Search&Ad_Content__c=534418150272&Ad_Term_s__c=&AdWords_Campaign_Name__c=&AdWords_ID__c=&AdWords_Keyword__c=&full_ref_url=unknown; _cq_duid=1.1719386881.yBiFbzwf2ogTjPBg; _cq_suid=1.1719386881.HZZFI0qVNdBB2CDv; ASP.NET_SessionId=jxnvupu24yl4bq3fxztuh0me; driftt_aid=7ce0118a-b0a0-4202-bbd5-a9a67ae08d9f; drift_aid=7ce0118a-b0a0-4202-bbd5-a9a67ae08d9f; JSESSIONID=D74A60423CF8389BBF14F679D97F4C26.10.58.59.41; SNLStack=STACK1; TRINITY_USER_DATA=eyJ1c2VySWRUUyI6MTczNjg0NjcyNzcyM30=; TRINITY_USER_ID=46f712c4-26eb-48b7-a7aa-97cabb614611; BNI_persistence=UeLbLrl1461xKZfyh1owx08wu-dxEHMOlnEKf9YF0tJa6jjkQ-juJum7RxvMF3dKDqOWwzI8A7gXhP9x0YhzCw==; s_dur=1738130703946; drift_campaign_refresh=6ccd23a4-80e2-4a1f-9662-a2a6fafa6412; search-token-test=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZWFyY2gtcXVlcnkiLCJjbGllbnQtaWQiOiJ3ZWItc2VhcmNoIiwiZXhwIjoxNzM4MTMxNzU0Mzg5fQ.R_ZqqC9d8HEpsMDWRbmiqNXeHiSGxqKGZTfSECKQMCQ; search-token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZWFyY2gtcXVlcnkiLCJjbGllbnQtaWQiOiJ3ZWItc2VhcmNoIiwiZXhwIjoxNzM4MTMxNzU0Mzg5fQ.R_ZqqC9d8HEpsMDWRbmiqNXeHiSGxqKGZTfSECKQMCQ; AWSALB=T/SMMgRrgoYpmJ3Dqp9PQPNrPnAFmHbURIbvVRqS1iHxETZki+w44uQ/8btfM9yztTMAYJtxzIxzi029Z/c/Ijtq/Li2eAU9CfyxqkWBVBfOAt6GZyW2SctTfMpD; AWSALBCORS=T/SMMgRrgoYpmJ3Dqp9PQPNrPnAFmHbURIbvVRqS1iHxETZki+w44uQ/8btfM9yztTMAYJtxzIxzi029Z/c/Ijtq/Li2eAU9CfyxqkWBVBfOAt6GZyW2SctTfMpD; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Jan+29+2025+10%3A05%3A33+GMT%2B0400+(Gulf+Standard+Time)&version=202409.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=9fddc8b1-c479-4b4f-a520-f5cab70c6cd6&interactionCount=1&isAnonUser=1&landingPath=https%3A%2F%2Fwww.spglobal.com%2Fen%2Fresearch-insights%2Fevents%2Ffeatured%23q%3D%26rows%3D20%26pagenum%3D1%26sort%3Des_event_start_date_dt%2520asc%26facets%3D%7B%2522es_event_end_date_dt%2522%3A%2522upcoming%2522%7D&groups=C0003%3A0%2CC0004%3A0%2CC0002%3A0%2CC0001%3A1; s_nr365=1738130733744-Repeat; s_tslv=1738130733746',
    'priority': 'u=1, i',
    'referer': 'https://www.spglobal.com/en/research-insights/events/featured',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print("Response status code (S&P):", response.status_code)

    data = response.json()
    source = "S&P"
    events = []
    for event in data.get('response', {}).get('docs', []):
        es_title_t = event.get('es_title_t', 'N/A')
        es_event_category_s = event.get('es_event_category_s', 'N/A')
        es_url_s = event.get('es_url_s', 'N/A')
        es_event_start_date_dt = event.get('es_event_start_date_dt', 'N/A')
        es_body_content_txt = event.get('es_body_content_txt', 'N/A')
        if es_event_start_date_dt != 'N/A':
            try:
                es_event_start_date_dt = datetime.strptime(es_event_start_date_dt, "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                es_event_start_date_dt = datetime.strptime(es_event_start_date_dt, "%Y-%m-%dT%H:%M:%SZ")
            month = es_event_start_date_dt.strftime("%B %Y")
        else:
            month = 'N/A'
        events.append({
                "Event Name": es_title_t,
                "Event URL": es_url_s,
                "Start Date": es_event_start_date_dt,
                "Venue Address": es_event_category_s,
                "Summary": es_body_content_txt,
                "Source": source,
                "Month": month
            })
    print("Total upcoming events (S&P):", len(events))
    return events