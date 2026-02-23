import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import logging
from utils.db import save_article

COVEO_API_URL = "https://imfproduction561s308u.org.coveo.com/rest/search/v2?organizationId=imfproduction561s308u"
COVEO_TOKEN = "Bearer xx742a6c66-f427-4f5a-ae1e-770dc7264e8a"

def fetch_imf_articles(iso_code, region="CentralAsia"):
    session = requests.Session()
    headers = {
        "Authorization": COVEO_TOKEN,
        "Content-Type": "application/json",
        "Referer": "https://www.imf.org/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    payload = {
        "locale": "en-US",
        "q": f"@imfisocode={iso_code} @imflanguage=ENG",
        "enableQuerySyntax": True,
        "searchHub": "Search",
        "sortCriteria": "@imfdate descending",
        "numberOfResults": 10,
        "firstResult": 0,
        "cq": "(@source==\"IMF-ORG\")",
        "fieldsToInclude": [
            "author", "language", "urihash", "objecttype", "collection", "source", 
            "permanentid", "imfcontenttype", "imfcountry", "imfdate", "imfdescription", "date"
        ]
    }

    try:
        response = session.post(COVEO_API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code != 200:
            print(f"Failed to retrieve IMF articles for {iso_code}. Status code: {response.status_code}")
            return []

        data = response.json()
        articles = []
        for item in data.get("results", []):
            title = item.get("title", "No Title")
            click_uri = item.get("clickUri")
            if not click_uri:
                continue
            
            # Convert imfdate (milliseconds) to YYYY-MM-DD
            raw_date_ms = item.get("raw", {}).get("imfdate")
            if raw_date_ms:
                formatted_date = datetime.fromtimestamp(raw_date_ms / 1000.0).strftime("%Y-%m-%d")
            else:
                formatted_date = datetime.now().strftime("%Y-%m-%d")

            # Fetch article content
            try:
                time.sleep(2)
                art_response = requests.get(click_uri, timeout=30)
                if art_response.status_code == 200:
                    soup = BeautifulSoup(art_response.text, "html.parser")
                    content_parts = []
                    
                    section = soup.select_one("section")
                    if section:
                        for child in section.children:
                            if child.name == "p":
                                content_parts.append(child.get_text(strip=True))
                            elif child.name == "ol":
                                for list_item in child.find_all("li"):
                                    content_parts.append(list_item.get_text(strip=True))
                    
                    if not content_parts:
                        summary_section = soup.select_one("section.publication-summary .publication-text")
                        if summary_section:
                            content_parts.append(summary_section.get_text(strip=True))
                    
                    if not content_parts:
                        meta_desc = soup.find("meta", attrs={"name": "description"})
                        if meta_desc:
                            content_parts.append(meta_desc.get("content", ""))

                    content = "\n\n".join(content_parts) if content_parts else "No content available"
                else:
                    content = f"No content available (Status {art_response.status_code})"
            except Exception as e:
                print(f"Error fetching content for {click_uri}: {e}")
                content = "No content available (Error)"

            articles_info = {
                "title": title,
                "link": click_uri,
                "date": formatted_date,
                "content": content,
                "source": "IMF",
                "region": region,
                "sector": "sovereigns",
                "keywords": None
            }
            save_article(articles_info)
            articles.append(articles_info)
        return articles
    except Exception as e:
        print(f"Error in fetch_imf_articles for {iso_code}: {e}")
        return []

def imf_uzb():
    return fetch_imf_articles("UZB")

def imf_kaz():
    return fetch_imf_articles("KAZ")

def imf_kgz():
    return fetch_imf_articles("KGZ")

def imf_arm():
    return fetch_imf_articles("ARM")

def imf_aze():
    return fetch_imf_articles("AZE")

def imf_ca_sov():
    articles = []
    articles.extend(imf_uzb())
    articles.extend(imf_kaz())
    articles.extend(imf_kgz())
    articles.extend(imf_arm())
    articles.extend(imf_aze())
    return articles
