import json
import logging
import requests
import cloudscraper
from datetime import datetime
from bs4 import BeautifulSoup
from utils.check import me_related
from utils.keywords import me_reuters_KEYWORDS

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# import undetected_chromedriver as uc
from selenium_stealth import stealth
import time
import os
from utils.db import save_article

def reuters_articles():
    url = "https://www.reuters.com/world/middle-east/"
    
    print("DEBUG: Starting Selenium for Reuters...")
    
    # Fallback to standard Selenium as UC failed in this env
    chrome_options = Options()
    # Headless mode is blocked by Datadome, using headful
    # chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        chromedriver_path = ChromeDriverManager().install()
        if "THIRD_PARTY_NOTICES.chromedriver" in chromedriver_path:
                chromedriver_path = chromedriver_path.replace("THIRD_PARTY_NOTICES.chromedriver", "chromedriver.exe")
    except:
        chromedriver_path = "chromedriver.exe"

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    try:
        # First visit the main page to establish session/cookies and pass potential challenges
        print("DEBUG: Visiting main page to establish session...")
        driver.get("https://www.reuters.com/world/middle-east/")
        time.sleep(15) # Increased wait for Datadome challenge
        
        # Now hit the API endpoint
        print("DEBUG: Fetching API data...")
        # Construct the API URL
        import urllib.parse
        query_params = {
            "arc-site": "reuters",
            "fetch_type": "collection",
            "offset": 0,
            "requestId": 2,
            "section_id": "/world/middle-east/",
            "size": 20,
            "uri": "/world/middle-east/",
            "website": "reuters"
        }
        encoded_query = urllib.parse.quote(json.dumps(query_params))
        api_url = f"https://www.reuters.com/pf/api/v3/content/fetch/articles-by-section-alias-or-id-v1?query={encoded_query}&d=337&mxId=00000000&_website=reuters"
        
        driver.get(api_url)
        time.sleep(3)
        
        # Get JSON content from body
        try:
            # Try to get text from pre tag (common for JSON responses in Chrome)
            try:
                body_text = driver.find_element("tag name", "pre").text
            except:
                body_text = driver.find_element("tag name", "body").text
            
            data = json.loads(body_text)
            
            articles_data = data.get('result', {}).get('articles', [])
            print(f"DEBUG: Found {len(articles_data)} articles from API")
            
            articles = []
            for article in articles_data:
                title = article.get('title')
                link = f"https://www.reuters.com{article.get('canonical_url')}"
                published_time = article.get('published_time', 'No publish time available.')
                try:
                    date = datetime.strptime(published_time.replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f")
                    formatted_date = date.strftime('%Y-%m-%d')
                except ValueError:
                    formatted_date = 'Invalid Date'
                
                paragraphs = []
                # We can try to get content from the API response if available, or fetch individually
                # The API response usually contains 'content_elements'
                if 'content_elements' in article:
                    for element in article['content_elements']:
                        if element.get('type') == 'text':
                            paragraphs.append(element.get('content', ''))
                
                # If no content in API, fetch the page (optional, might be slow/blocked)
                if not paragraphs:
                    try:
                        driver.get(link)
                        time.sleep(2)
                        article_soup = BeautifulSoup(driver.page_source, 'html.parser')
                        article_body = article_soup.find('div', {'data-testid': 'ArticleBody'})
                        if article_body:
                            paragraphs = [p.get_text(strip=True) for p in article_body.find_all('div', {'data-testid': lambda x: x and x.startswith('paragraph-')})]
                    except Exception as e:
                        print(f"DEBUG: Error fetching article content {link}: {e}")

                matched_keywords = me_related(title, paragraphs, me_reuters_KEYWORDS)
                if not matched_keywords:
                    continue
                
                articles.append({
                    'title': title,
                    'link': link,
                    'content': paragraphs,
                    'date': formatted_date,
                    'source': 'Reuters',
                    'keywords': matched_keywords,
                    'region': 'MiddleEast',
                    'sector': 'banks'
                })
            save_article(articles)
            return articles

        except json.JSONDecodeError:
            print("DEBUG: Failed to decode JSON from API response. Falling back to HTML parsing...")
            # If API fails, we are already on the page (or can go back)
            driver.get("https://www.reuters.com/world/middle-east/")
            time.sleep(5)
            
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
        
        # Try to find the script tag again, or parse HTML directly if script is missing/obfuscated
        script_tag = soup.find('script', id='fusion-metadata', type='application/javascript')

        if script_tag:
            script_content = script_tag.string
            start_index = script_content.find('Fusion.globalContent=') + len('Fusion.globalContent=')
            end_index = script_content.find(';', start_index)
            json_data = script_content[start_index:end_index].strip()
            try:
                data = json.loads(json_data)
                articles_data = data.get('result', {}).get('articles', [])
                articles = []
                for article in articles_data:
                    title = article.get('title')
                    link = f"https://www.reuters.com{article.get('canonical_url')}"
                    published_time = article.get('published_time', 'No publish time available.')
                    try:
                        date = datetime.strptime(published_time.replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f")
                        formatted_date = date.strftime('%Y-%m-%d')
                    except ValueError:
                        formatted_date = 'Invalid Date'
                    
                    paragraphs = []
                    try:
                        driver.get(link)
                        time.sleep(2)
                        article_soup = BeautifulSoup(driver.page_source, 'html.parser')
                        article_body = article_soup.find('div', {'data-testid': 'ArticleBody'})
                        if article_body:
                            paragraphs = [p.get_text(strip=True) for p in article_body.find_all('div', {'data-testid': lambda x: x and x.startswith('paragraph-')})]
                    except Exception as e:
                        print(f"DEBUG: Error fetching article content {link}: {e}")

                    matched_keywords = me_related(title, paragraphs, me_reuters_KEYWORDS)
                    if not matched_keywords:
                        # logging.debug(f"Skipping non-relevant article: {title}")
                        pass
                    
                    articles_data = ({
                        'title': title,
                        'link': link,
                        'content': paragraphs,
                        'date': formatted_date,
                        'source': 'Reuters',
                        'keywords': matched_keywords,
                        'region': 'MiddleEast',
                        'sector': 'banks'
                    })
                    articles.append(articles_data)

                return articles
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return []
        else:
            # Fallback: Parse HTML directly if JSON is missing
            print("DEBUG: JSON metadata not found, parsing HTML directly...")
            articles = []
            # Updated selector for Reuters new layout
            # Try multiple potential selectors for article cards
            article_cards = soup.find_all('li', class_=lambda x: x and 'story-card' in x)
            if not article_cards:
                 article_cards = soup.find_all('div', class_=lambda x: x and 'media-story-card' in x)
            if not article_cards:
                 # Generic fallback for list items with links
                 article_cards = [li for li in soup.find_all('li') if li.find('h3') or (li.find('a') and len(li.get_text()) > 50)]
            
            # Debug: Print page title to see if we are blocked or on wrong page
            print(f"DEBUG: Page Title: {soup.title.string if soup.title else 'No Title'}")
            print(f"DEBUG: Found {len(article_cards)} cards.")
            
            for card in article_cards:
                try:
                    title_tag = card.find('a', {'data-testid': 'Heading'}) or card.find('h3', {'data-testid': 'Heading'})
                    if not title_tag: 
                        # Try finding any link with text inside the card
                        links = card.find_all('a')
                        for l in links:
                            if l.get_text(strip=True) and len(l.get_text(strip=True)) > 20:
                                title_tag = l
                                break
                    
                    if not title_tag: continue
                    
                    title = title_tag.get_text(strip=True)
                    link = title_tag['href'] if title_tag.name == 'a' else title_tag.find_parent('a')['href']
                    
                    if not link.startswith('http'):
                        link = "https://www.reuters.com" + link
                        
                    time_tag = card.find('time')
                    date_str = time_tag['datetime'] if time_tag else datetime.now().isoformat()
                    try:
                        date = datetime.strptime(date_str.replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f")
                        formatted_date = date.strftime('%Y-%m-%d')
                    except:
                        formatted_date = datetime.now().strftime('%Y-%m-%d')

                    paragraphs = []
                    try:
                        driver.get(link)
                        time.sleep(2)
                        article_soup = BeautifulSoup(driver.page_source, 'html.parser')
                        article_body = article_soup.find('div', {'data-testid': 'ArticleBody'}) or article_soup.find('article')
                        if article_body:
                            paragraphs = [p.get_text(strip=True) for p in article_body.find_all('p')]
                    except Exception as e:
                        print(f"DEBUG: Error fetching article content {link}: {e}")

                    matched_keywords = me_related(title, paragraphs, me_reuters_KEYWORDS)
                    if not matched_keywords:
                        continue
                        
                    articles_data = ({
                        'title': title,
                        'link': link,
                        'content': paragraphs,
                        'date': formatted_date,
                        'source': 'Reuters',
                        'keywords': matched_keywords,
                        'region': 'MiddleEast',
                        'sector': 'banks'
                    })
                    articles.append(articles_data)
                except Exception as e:
                    print(f"DEBUG: Error parsing card: {e}")
                    continue
            
            return articles
            
    except Exception as e:
        print(f"DEBUG: Selenium error: {e}")
        return []
    finally:
        driver.quit()