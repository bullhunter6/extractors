import requests
from bs4 import BeautifulSoup
from dateutil import parser
import re
from utils.db import save_events

def moodys_events():
    url = "https://events.moodys.com/"

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    event_cards = soup.find_all("div", class_="event-horizontal-card")

    events = []

    def preprocess_date(date_text):
        clean_date = re.sub(r'event\s+', '', date_text)
        clean_date = re.sub(r'\s+', ' ', clean_date).strip()
        clean_date = re.split(r'\||-|\d{1,2}[:.]\d{2}', clean_date)[0].strip()
        return clean_date

    for card in event_cards:
        title_element = card.find("h3", class_="event-horizontal-card__title")
        title = title_element.text.strip() if title_element else "N/A"
        if not title.isascii():
            continue

        link = card.find("a", href=True)["href"] if card.find("a", href=True) else "N/A"
        time_element = card.find("time", class_="event-horizontal-card__date")
        date = "N/A"

        if time_element:
            date_text = time_element.text.strip()
            clean_date_text = preprocess_date(date_text)
            try:
                formatted_date = parser.parse(clean_date_text).strftime("%Y-%m-%d")
                date = formatted_date
            except ValueError:
                print(f"Warning: Could not parse date '{clean_date_text}'. Using original format.")
                date = clean_date_text

        location_element = card.find("div", class_="event-horizontal-card__image__badge")
        location = location_element.text.strip() if location_element else "N/A"

        events.append({
            "title": title,
            "link": link,
            "date": date,
            "location": location,
            "details": "N/A"
        })
        save_events(events, source="Moody's")
    return events