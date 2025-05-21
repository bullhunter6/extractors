import requests
import json
from datetime import datetime
from utils.db_utils import save_article

def fetch_all_article_slugs():
    url = "https://api.fitchratings.com/"
    
    # Initial request to get multiple articles with their slugs
    payload = json.dumps({
        "query": """
        query SFInsights($language: String, $reportType: String, $sector: String, $limit: Int) {
          getSFInsights(
            language: $language
            reportType: $reportType
            sector: $sector
            limit: $limit
          ) {
            rows {
              slug
              title
              publishedDate
            }
          }
        }""",
        "variables": {
            "language": "",
            "reportType": "insights/sustainable-insight,insights/commentary,insights/esg-rating,insights/second-party-opinion",
            "limit": 10  # You can adjust this limit as needed
        }
    })
    
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.sustainablefitch.com',
        'priority': 'u=1, i',
        'referer': 'https://www.sustainablefitch.com/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Cookie': 'SSID_P=CQCoQB1GAAQAAACgzzlm4GeAA6DPOWYWAAAAAAAAAAAAcRUjZwC33yoAAAELBQAAcRUjZwEAjgAAAXUUAABxFSNnAQCSAAADRRUAAHEVI2cBAIsAAAHJEwAAcRUjZwEAeAAAARwRAABxFSNnAQB0AAAA; SSOD_P=ABG_AAAAEgC6AAAAEQAAAKDPOWYRJVhmAAAAAA; SSRT_P=cPwpZwADAA'
    }

    response = requests.post(url, headers=headers, data=payload)
    data = response.json()
    
    # Extracting slugs for each article
    return data.get("data", {}).get("getSFInsights", {}).get("rows", [])

def fetch_article_details(slug):
    url = "https://api.fitchratings.com/"
    
    # Payload for fetching article details by slug
    payload = json.dumps({
        "query": """
        query RAC($slug: String!) {
          getSFResearchItem(slug: $slug) {
            abstract
            publishedDate
            marketing {
              displayTitle
              openGraphTags {
                url
              }
            }
            paragraphs {
              content
            }
          }
        }""",
        "variables": {
            "slug": slug
        }
    })
    
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.sustainablefitch.com',
        'priority': 'u=1, i',
        'referer': 'https://www.sustainablefitch.com/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Cookie': 'SSID_P=CQCoQB1GAAQAAACgzzlm4GeAA6DPOWYWAAAAAAAAAAAAcRUjZwC33yoAAAELBQAAcRUjZwEAjgAAAXUUAABxFSNnAQCSAAADRRUAAHEVI2cBAIsAAAHJEwAAcRUjZwEAeAAAARwRAABxFSNnAQB0AAAA; SSOD_P=ABG_AAAAEgC6AAAAEQAAAKDPOWYRJVhmAAAAAA; SSRT_P=cPwpZwADAA'
    }


    response = requests.post(url, headers=headers, data=payload)
    article_data = response.json().get("data", {}).get("getSFResearchItem", {})

    title = article_data.get("marketing", {}).get("displayTitle", "No Title")
    abstract = article_data.get("abstract", "No Abstract")

    published_date = article_data.get("publishedDate", "")
    if published_date:
        date_obj = datetime.fromisoformat(published_date.replace("Z", "+00:00"))
        formatted_date = date_obj.strftime("%Y-%m-%d")
    else:
        formatted_date = "Unknown Date"

    url_slug = article_data.get("marketing", {}).get("openGraphTags", {}).get("url", "")
    full_url = f"https://www.sustainablefitch.com/{url_slug}" if url_slug else "No URL"
    
    paragraphs = article_data.get("paragraphs", [])
    full_summary = " ".join(p.get("content", "").strip() for p in paragraphs if p.get("content"))

    article_info = {
        "title": title,
        "date": formatted_date,
        "url": full_url,
        "summary": full_summary,
        "source": "Sustainable Fitch",
        "keywords": "No Keywords"
    }
    
    return article_info

def sustainablefitch_articles():
    articles = []
    article_slugs = fetch_all_article_slugs()
    
    for article_meta in article_slugs:
        slug = article_meta.get("slug")
        article_info = fetch_article_details(slug)
        save_article(article_info)
        articles.append(article_info)
    
    return articles
