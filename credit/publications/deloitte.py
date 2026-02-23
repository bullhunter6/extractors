import requests
from bs4 import BeautifulSoup
from utils.db import save_publication

def deloitte_publications():
    url = "https://www.deloitte.com/middle-east/en/our-thinking/mepov-magazine.html"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    article_containers = soup.find_all('a', class_='cmp-promo-tracking')

    articles = []
    for container in article_containers:
        title_element = container.find('h3', class_='cmp-promo__content__title')
        title = title_element.get_text(strip=True) if title_element else "No title"
        desc_element = container.find('div', class_='cmp-promo__content__desc')
        description = desc_element.get_text(strip=True) if desc_element else "No description"
        link = container['href']
        full_link = f"https://www.deloitte.com{link}" if link.startswith("/") else link

        image_element = container.find('img', class_='js-image-rendition')
        image_url = image_element['src'] if image_element else "No image"

        article = {
            'title': title,
            'description': description,
            'link': full_link,
            'image': image_url,
            'date': None
        }
        articles.append(article)
        # Save each article individually
        save_publication(article, source="deloitte")
        
    return articles

