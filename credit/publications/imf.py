import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry
from utils.db import save_publication

def imf_weo_publications():
    url = "https://www.imf.org/en/Publications/WEO"
    base_url = "https://www.imf.org"
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=2, status_forcelist=[500, 502, 503, 504],allowed_methods=["GET"])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    target_div = soup.find('div', class_='module search-info')
    weo_main = {}
    if target_div:
        weo_main['title'] = target_div.find('h2').text.strip()
        gray_box = target_div.find('div', class_='gray-box')
        weo_main['description'] = gray_box.text.strip() if gray_box else "No description available"
        link_tag = target_div.find('a')
        weo_main['link'] = base_url + link_tag['href'].strip() if link_tag else "#"
        date_tag = target_div.find('p', class_='date')
        weo_main['date'] = date_tag.text.strip() if date_tag else "No date available"
    publications = []
    pub_rows = soup.find_all('div', class_='result-row pub-row')
    for row in pub_rows:
        title_tag = row.find('a')
        title = title_tag.text.strip() if title_tag else "No title"
        link = base_url + title_tag['href'].strip() if title_tag else "No link"
        
        date_tag = row.find_all('p')[0]
        date = date_tag.text.strip() if date_tag else "No date"
        
        description_tag = row.find('span')
        description = description_tag.text.strip() if description_tag else "No description"
        
        img_tag = row.find('img')
        img_url = "https://www.imf.org/" + img_tag['src'].strip() if img_tag else "No image"
        
        publication = {
            'title': title,
            'link': link,
            'date': date,
            'description': description,
            'image': img_url
        }
        publications.append(publication)
        save_publication(publication, source="IMF weo")
    return publications

def imf_reo_publications():
    url = "https://www.imf.org/en/Publications/REO"
    base_url = "https://www.imf.org"

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=2, status_forcelist=[500, 502, 503, 504],allowed_methods=["GET"])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    
    try:
        response = session.get(url,timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    target_div = soup.find('div', class_='module search-info')
    reo_main = {}
    if target_div:
        reo_main['title'] = target_div.find('h2').text.strip()
        gray_box = target_div.find('div', class_='gray-box')
        reo_main['description'] = gray_box.text.strip() if gray_box else "No description available"
    publications = []
    pub_rows = soup.find_all('div', class_='result-row pub-row')
    for row in pub_rows:
        title_tag = row.find('a')
        title = title_tag.text.strip() if title_tag else "No title"
        link = base_url + title_tag['href'].strip() if title_tag else "No link"
        
        date_tag = row.find_all('p')[0]
        date = date_tag.text.strip() if date_tag else "No date"
        
        description_tag = row.find('span')
        description = description_tag.text.strip() if description_tag else "No description"
        
        img_tag = row.find('img')
        img_url = "https://www.imf.org/" + img_tag['src'].strip() if img_tag else "No image"
        
        publication = {
            'title': title,
            'link': link,
            'date': date,
            'description': description,
            'image': img_url
        }
        publications.append(publication)
        save_publication(publication, source="IMF reo")
    return publications


def imf_gfsr_publications():
    url = "https://www.imf.org/en/Publications/GFSR"
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=2, status_forcelist=[500, 502, 503, 504],allowed_methods=["GET"])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    target_div = soup.find('div', class_='module search-info')
    gfsr_main = {}
    if target_div:
        gfsr_main['title'] = target_div.find('h2').text.strip()
        gfsr_main['description'] = target_div.find('p').text.strip()

    publications = []
    pub_rows = soup.find_all('div', class_='result-row pub-row')
    for row in pub_rows:
        
        title_tag = row.find('a')
        title = title_tag.text.strip() if title_tag else "No title"
        
        link = "https://www.imf.org" + title_tag['href'].strip() if title_tag else "No link"
        
        date_tag = row.find_all('p')[0]
        date = date_tag.text.strip() if date_tag else "No date"
        
        description_tag = row.find('span')
        description = description_tag.text.strip() if description_tag else "No description"
        
        img_tag = row.find('img')
        img_url = "https://www.imf.org/" + img_tag['src'].strip() if img_tag else "No image"

        publication = {
            'title': title,
            'link': link,
            'date': date,
            'description': description,
            'image': img_url
        }
        publications.append(publication)
        save_publication(publication, source="IMF gfsr")
    return publications
