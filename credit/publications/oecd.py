import requests
from utils.db import save_publication

def oecd_publications():
    url = "https://aemint-search-client-funcapp-prod.azurewebsites.net/api/faceted-search?siteName=oecd&interfaceLanguage=en&orderBy=mostRelevant&pageSize=10&hiddenFacets=oecd-content-types%3Apublications%2Freports&hiddenFacets=oecd-content-types%3Apublications%2Fworking-papers"

    payload = {}
    headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://www.oecd.org',
    'Referer': 'https://www.oecd.org/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    publications = []
    data = response.json()
    results = data.get("results", [])
    for result in results:
        title = result.get("title", "No title available")
        description = result.get("description", "No description available")
        date = result.get("publicationDateTime", "No date available")
        link = result.get("url", "No link available")
        image = result.get("featuredImageUrl", "No image available")

        publication = {
            'title': title,
            'description': description,
            'date': date,
            'link': link,
            'image': image
        }
        publications.append(publication)
        save_publication(publication, source="oecd")
    return publications