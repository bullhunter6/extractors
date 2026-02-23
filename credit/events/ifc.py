import requests
import json
from bs4 import BeautifulSoup
from utils.db import save_events

def get_location(url):
    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.ifc.org/en/search?contentType=Event&language=English',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Cookie': 'AWSALB=Rnb4r408S3ZrhUYtUEsea35tP1RITqED9y05nsvs152uVpZpoppRKLsNEN967mF7su2BH0dTc7SsMRUU/ZcgeC54p0zh008h7pzb862JtnECLrGQilg/dvBUim9F; AWSALBCORS=Rnb4r408S3ZrhUYtUEsea35tP1RITqED9y05nsvs152uVpZpoppRKLsNEN967mF7su2BH0dTc7SsMRUU/ZcgeC54p0zh008h7pzb862JtnECLrGQilg/dvBUim9F'
    }

    try:
        response = requests.get(url, headers=headers, data=payload)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            content_div = soup.find('div', class_='ifc__stats')
            if content_div:
                list_items = content_div.find_all('li')
                if len(list_items) > 1:
                    location = list_items[1].find('div', class_='ifc__stats_detail').text.strip()
                    return location
                
            teaser_description = soup.find('div', class_='cmp-teaser__description')
            if teaser_description:
                where_p = teaser_description.find_all('p')
                for p in where_p:
                    if "Where:" in p.text:
                        location = p.text.split("Where:")[-1].strip()
                        return location
            cmp_text = soup.find('div', class_='cmp-text')
            if cmp_text:
                where_p = cmp_text.find_all('p')
                for p in where_p:
                    bold_tag = p.find('b')
                    if bold_tag and "Where:" in bold_tag.text.replace("\xa0", " ").strip():
                        location = p.text.split("Where:")[-1].strip()
                        return location

        return "Location Not Available"
    except Exception as e:
        print(f"Error fetching location from {url}: {e}")
        return "Location Not Available"

def ifc_events():

    url = "https://webapi.worldbank.org/aemsite/ifc/search"
    payload = json.dumps({
    "search": "*",
    "facets": [
        "contentType,sort:value,count:10000",
        "countries,sort:value,count:10000",
        "topics,sort:value,count:10000",
        "regions,sort:value,count:10000",
        "subTopics,sort:value,count:10000",
        "language,sort:value,count:10000"
    ],
    "filter": "(contentType eq 'Event') and (language eq 'English')",
    "count": True,
    "top": 20,
    "skip": 0,
    "orderby": "contentDate desc"
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
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.post(url, headers=headers, data=payload)
    events = []
    if response.status_code == 200:
        data = response.json()
        for event in data.get('value', []):
            title = event.get('title', 'N/A')
            description = event.get('description', 'N/A')
            content_date = event.get('contentDate', 'N/A')
            page_path = event.get('pagePublishPath', 'N/A')
            location = "Location Not Available"
            events.append({
                'title': title,
                'date': content_date,
                'location': location,
                'details': description,
                'link': f"https://www.ifc.org{page_path}",
                'source': "IFC",
            })
    save_events(events, source="IFC")
    return events