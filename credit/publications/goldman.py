import requests
from datetime import datetime
from utils.db import save_publication

def goldmansachs_publications():
    url = "https://www.goldmansachs.com/feeds/insights.json"
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=1, i',
        'referer': 'https://www.goldmansachs.com/insights/goldman-sachs-research',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Handle both list and dict responses
        publications = data if isinstance(data, list) else data.get('items', data.get('data', []))
        if not isinstance(publications, list):
            print(f"Unexpected response format: {type(publications)}")
            return []
        results = []
        for pub in publications:
            content_types = pub.get("cmsPageProps", {}).get("contentType", [])
            is_report = any(ct.get("id") == "gscom:content-type/report" for ct in content_types)
            if not is_report:
                continue
            title = pub.get("title")
            last_modified_timestamp = pub.get("lastModifiedDate")
            if last_modified_timestamp:
                date = datetime.utcfromtimestamp(last_modified_timestamp / 1000).strftime('%Y-%m-%d')
            else:
                date = None
            link = f"https://www.goldmansachs.com{pub.get('path', '')}"
            image_info = pub.get("cmsPageProps", {}).get("oneIsToOneImage")
            image_link = f"https://www.goldmansachs.com{image_info['path']}" if image_info else None

            description = pub.get("description")
            publication = {
                "title": title,
                "date": date,
                "link": link,
                "image": image_link,
                "description": description
            }
            results.append(publication)
            # Save each publication individually
            save_publication(publication, source="goldmansachs")

        results = sorted(results, key=lambda x: x["date"], reverse=True)[:15]
    return results