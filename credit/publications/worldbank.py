import requests
from bs4 import BeautifulSoup
from utils.db import save_publication

def worldbank_publications():
    url = "https://www.worldbank.org/en/research"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    article_containers = soup.find_all('div', class_='lp__primary_card')

    articles = []
    for container in article_containers:
        title_element = container.find('h3', class_='lp__card_title')
        title = title_element.get_text(strip=True) if title_element else "No title"

        desc_element = container.find('div', class_='lp__card_description')
        description = desc_element.get_text(strip=True) if desc_element else "No description"

        link_element = container.find('a')
        link = link_element['href'] if link_element else "No link"

        image_element = container.find('img')
        image_url = image_element['data-srcset'] if image_element else "No image"

        article = {
            'title': title,
            'description': description,
            'link': link,
            'image': image_url,
            'date': None
        }
        articles.append(article)
        save_publication(article, source="worldbank")
    return articles


