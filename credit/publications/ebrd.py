import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils.db import save_publication

def ebrd_publications():
    url = "https://www.ebrd.com/publications"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    }

    BASE_URL = "https://www.ebrd.com"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.text, "html.parser")
        publications = []
        
        # Find all publication items
        pub_items = soup.find_all("div", class_="publication-item")
        
        for item in pub_items:
            try:
                # Get title and link
                title_elem = item.find("h3")
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                link_elem = title_elem.find("a")
                if not link_elem:
                    continue
                    
                link = link_elem.get("href", "")
                if not link.startswith("http"):
                    link = urljoin(BASE_URL, link)
                
                # Get date
                date_elem = item.find("div", class_="date")
                date = date_elem.get_text(strip=True) if date_elem else "No date found"
                
                # Get description
                desc_elem = item.find("div", class_="description")
                description = desc_elem.get_text(strip=True) if desc_elem else "No description found"
                
                # Get image
                img_elem = item.find("img")
                image_url = img_elem.get("src", "") if img_elem else ""
                if image_url and not image_url.startswith("http"):
                    image_url = urljoin(BASE_URL, image_url)
                
                if title and link and description:
                    publication = {
                        "title": title,
                        "link": link,
                        "image": image_url,
                        "description": description,
                        "date": date
                    }
                    publications.append(publication)
                    save_publication(publication, source="ebrd")
                    
            except Exception as e:
                print(f"Error processing publication item: {str(e)}")
                continue
                
        return publications
        
    except requests.RequestException as e:
        print(f"Error fetching EBRD publications: {str(e)}")
        return []
