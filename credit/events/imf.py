import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils.db import save_events


def imf_events():
    try:
        url = "https://www.imf.org/en/News/Seminars"

        headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        event_containers = soup.find_all('div', class_='result-row')
        events = []
        for event in event_containers:
            date_tag = event.find('p', class_='date')
            date = date_tag.text.strip() if date_tag else "N/A"
            title_tag = event.find('h6').find('a') if event.find('h6') else None
            title = title_tag.text.strip() if title_tag else "N/A"
            link = urljoin(url, title_tag['href'].strip()) if title_tag else "N/A"
            location_tag = event.find_all('p')[-1].find('a') if event.find_all('p') else None
            location = location_tag.text.strip() if location_tag else "N/A"
            events.append({
                'title': title,
                'date': date,
                'location': location,
                'details': "N/A",
                'link': link,
                'source': "IMF",
            })
        save_events(events, source="IMF")
        return events
    except Exception as e:
        print(f"IMF Events Error: {e}")
        return []
