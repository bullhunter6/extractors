import requests
from bs4 import BeautifulSoup
from utils.db import save_events


def adb_events():
    url = "https://www.adb.org/news/events/calendar"

    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    events = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        event_divs = soup.find_all("div", class_="clearfix")
        for event in event_divs:
            title = event.find("span", class_="event-title").get_text(strip=True) if event.find("span", class_="event-title") else "N/A"
            date = event.find("span", class_="event-date").get_text(strip=True) if event.find("span", class_="event-date") else "N/A"
            location = event.find("span", class_="event-location").get_text(strip=True) if event.find("span", class_="event-location") else "N/A"
            link = event.find("a", href=True)
            full_link = f"https://www.adb.org{link['href']}" if link else "N/A"
            events.append({
                'title': title,
                'date': date,
                'location': location,
                'details': "N/A",
                'link': full_link,
                'source': "ADB",
            })
    save_events(events, source="ADB")
    return events
