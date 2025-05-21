import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.db_utils import save_pub

def sustainalytics_pub():
    url = "https://www.sustainalytics.com/esg-research"
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.content, 'html.parser')
    blog_items = soup.find_all('div', class_='col-12 col-sm-6 col-md-4 col-lg-3 sust-blog-item-col')
    articles = []
    for blog_item in blog_items:
        image = blog_item.find('img', class_='embed-responsive-item')['src']
        title = blog_item.find('p', class_='card-title').text.strip()
        summary = blog_item.find('p', class_='card-text').text.strip()
        link = blog_item.find('a', class_='card-footer-link')['href']
        if not link.startswith('http'):
            link = "https://www.sustainalytics.com" + link
        source = 'Sustainalytics'
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        article = {
            'title': title,
            'summary': summary,
            'link': link,
            'source': source,
            'image_url': image,
            'date': date
        }
        save_pub(article)
        articles.append(article)
    return articles