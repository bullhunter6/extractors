import requests
from datetime import datetime, timezone
from utils.db import save_events


def fitch_events():
    try:
        url = "https://www.fitchratings.com/page-data/events/page-data.json"
        headers = {
            'accept': '*/*',
            'referer': 'https://www.fitchratings.com/events',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        response = requests.get(url, headers=headers)
        events = []
        if response.status_code == 200:
            data = response.json()
            current_time = datetime.now(timezone.utc)
            for event in data['result']['data']['allContentfulEvent']['nodes']:
                start_date = event.get('startDate', '')
                if start_date.endswith("Z"):
                    start_date = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
                else:
                    start_date = datetime.fromisoformat(start_date).replace(tzinfo=timezone.utc)
                if start_date > current_time:
                    events.append({
                        'title': event.get('title', 'N/A'),
                        'date': start_date.isoformat(),
                        'location': event.get('locationName', 'N/A'),
                        'details': "N/A",
                        'link': f"https://events.fitchratings.com{event.get('relativeVanityUrl', '')}",
                        'source': "Fitch",
                    })
        save_events(events, source="Fitch")
        return events
    except Exception as e:
        print(f"Fitch Events Error: {e}")
        return []