import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.db import save_events

def bloomberg_events_1():
    url = "https://www.bloomberglive.com/calendar/"

    payload = {}
    headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-US,en;q=0.9',
      'cookie': '_dd_s=logs=1&id=9385c3f9-18e7-4b7f-8076-90bf69311d62&created=1737353022467&expire=1737353922467',
      'priority': 'u=0, i',
      'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'none',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    event_tiles = soup.find_all('article', id=lambda x: x and x.startswith('event-tile'))

    events = []

    for tile in event_tiles:
        link_tag = tile.find('a', href=True)
        link = link_tag['href'] if link_tag else None
        date_tag = tile.find('div', class_='date')
        date = date_tag.text.strip() if date_tag else None
        location_tag = tile.find('div', class_='city')
        location = location_tag.text.strip() if location_tag else None
        title_tag = tile.find('h2', class_='content')
        title = title_tag.text.strip() if title_tag else None
        footer_tag = tile.find('div', class_='footer')
        topics = footer_tag.text.strip() if footer_tag else None

        events.append({
            'title': title,
            'date': date,
            'location': location,
            'details': topics,
            'link': link,
            'source': 'Bloomberg'
        })

    current_date = datetime.now()

    filtered_events = []

    for event in events:
        raw_date = event['date']

        if '-' in raw_date:
            start_date_str, _ = raw_date.split('-')
            if ',' in raw_date:
                _, year_str = raw_date.split(',')
                year = int(year_str.strip())
            else:
                year = current_date.year
            start_date_str = start_date_str.strip() + f", {year}"
        else:
            start_date_str = raw_date.strip()

        start_date = datetime.strptime(start_date_str, '%B %d, %Y')
        if start_date >= current_date:
            event['date'] = start_date.strftime('%Y-%m-%d')
            filtered_events.append(event)
            save_events(filtered_events, source='Bloomberg')
    return filtered_events


def bloomberg_events_2():
    url = "https://www.bloomberg.com/professional/insights/webinars/all/?lang=english"
    headers = {
        'Referer': 'https://www.bloomberg.com/professional/insights/webinars/all/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        webinar_blocks = soup.find_all('div', class_='webinar-block')

        events = []
        for block in webinar_blocks:
            title_tag = block.find('div', class_='title').find('a')
            title = title_tag.text.strip() if title_tag else None
            link = title_tag['href'] if title_tag and title_tag.has_attr('href') else None
            date_tag = block.find('span', class_='date')
            raw_date = date_tag.text.strip() if date_tag else None
            date = None
            if raw_date:
                try:
                    date = datetime.strptime(f"{raw_date}, {datetime.now().year}", "%B %d, %Y").strftime("%Y-%m-%d")
                except ValueError:
                    pass


            events.append({
                'title': title,
                'date': date,
                'link': link,
                'location': 'Webinar',
                'details': 'N/A',
                'source': 'Bloomberg'
            })
        save_events(events, source='Bloomberg')
    return events


def bloomberg_events():
    events_1 = bloomberg_events_1()
    events_2 = bloomberg_events_2()

    return events_1 + events_2