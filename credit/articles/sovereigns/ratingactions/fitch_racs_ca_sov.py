import requests
import json
import logging
from bs4 import BeautifulSoup
from utils.db import save_article


def fitch_racs_content(slug):
    url = "https://api.fitchratings.com/"
    payload = json.dumps({
        "query": """
        query RAC($slug: String!) {
            getResearchItem(slug: $slug) {
                abstract
                marketing {
                    displayEnglishTitle
                    metadataTags {
                        description
                    }
                }
                paragraphs {
                    content
                }
            }
        }
        """,
        "variables": {"slug": slug}
    })

    headers = {
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/json',
      'cookie': '_hjSessionUser_2372539=eyJpZCI6IjM0YmI2Y2JjLTdlYzktNWU5NS1hM2U4LWMwYjJmOWYxYmI4MCIsImNyZWF0ZWQiOjE3MTUwNjQ3MzYzMjcsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.1.1774897111.1715064736; _mkto_trk=id:732-CKH-767&token:_mch-fitchratings.com-1715064737028-35924; cb_user_id=null; cb_group_id=null; cb_anonymous_id=%2246615693-8036-40f6-a981-af102a853a5b%22; _gcl_au=1.1.1108227181.1730352392; SSSC_P=1.G7366146951701620704.30|42.1291:120.4381:139.5066:142.5228:146.5445; _hjSession_2372539=eyJpZCI6ImI4NzYyYTYyLTQ0MTAtNDQ2ZS1iYmFiLTQ3YjcyZDhkNjVjNiIsImMiOjE3MzI3MDQ5NTQyMjksInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; SSRT_P=vfxGZwADAA; SSOD_P=ALUtAAAAEgC6AAAAMAAAAKDPOWa9_EZnAwAAAA; SSID_P=CQCNgB1GAAQAAACgzzlm4GeAA6DPOWYeAAAAAAAAAAAAuPpGZwC33yoAAAELBQAAuPpGZwEAjgAAAWwUAAC4-kZnAQCLAAAByhMAALj6RmcBAHgAAAEdEQAAuPpGZwEAkgAAA0UVAABxFSNnCQB0AAAA; _ga_E58YZGKRFB=GS1.1.1732704954.39.1.1732705470.56.0.0; is=595c750e-d9ad-49d8-a318-b6b10acaf059; iv=620091d7-e4e6-4cc6-b23f-ba42669134ad; SSID_P=CQCqWB1GAAQAAACgzzlm4GeAA6DPOWYeAAAAAAAAAAAAuPpGZwC33yoAAAELBQAAuPpGZwEAkgAAA0UVAABxFSNnCQB4AAABHREAALj6RmcBAI4AAAFsFAAAuPpGZwEAiwAAAcoTAAC4-kZnAQB0AAAA; SSOD_P=ALUtAAAAEgC6AAAAMAAAAKDPOWa9_EZnAwAAAA; SSRT_P=ogBHZwADAA; SSSC_P=1.G7366146951701620704.30|42.1291:120.4381:139.5066:142.5228:146.5445',
      'origin': 'https://www.fitchratings.com',
      'priority': 'u=1, i',
      'referer': 'https://www.fitchratings.com/',
      'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code != 200:
        return {"error": f"Failed to fetch data. HTTP Status Code: {response.status_code}"}
    data = response.json()
    research_item = data.get("data", {}).get("getResearchItem", {})
    paragraphs = [p.get("content", "").strip() for p in research_item.get("paragraphs", []) if p.get("content")]

    full_content = "\n\n".join(filter(None,paragraphs))

    return full_content

def fitch_reporturl_content(slug):
    url = "https://api.fitchratings.com/"
    payload = json.dumps({
        "query": """
        query RAC($slug: String!) {
            getResearchItem(slug: $slug) {
                reportURL
                abstract
                title
            }
        }
        """,
        "variables": {"slug": slug}
    })

    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'origin': 'https://www.fitchratings.com',
        'referer': 'https://www.fitchratings.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code != 200:
            return {"error": f"Failed to fetch data. HTTP Status Code: {response.status_code}"}
        data = response.json()
        report_url = data.get("data", {}).get("getResearchItem", {}).get("reportURL")
        return f'Report Link: {report_url}'

    except requests.RequestException as e:
        return {"error": f"Request failed: {e}"}

    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse JSON response: {e}"}

def clean_html_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    for p_tag in soup.find_all("p"):
        p_tag.insert_before("\n")
    clean_text = soup.get_text(separator=" ", strip=True)
    return clean_text

def fitch_racs_ca_sov():
    url = "https://api.fitchratings.com/"
    payload = json.dumps({
        "query": """
        query Search($item: SearchItem, $term: String!, $filter: SearchFilterInput, $sort: String, $dateRange: String, $offset: Int, $limit: Int) {
            search(item: $item term: $term filter: $filter sort: $sort dateRange: $dateRange offset: $offset limit: $limit) {
                research {
                    title
                    permalink
                    publishedDate
                    abstract
                }
                racs {
                    title
                    permalink
                    publishedDate
                    abstract
                }
            }
        }
        """,
        "variables": {
            "item": "ALL",
            "term": "",
            "filter": {
                "country": [
                    "",
                    "Kazakhstan",
                    "Uzbekistan",
                    "Tajikistan",
                    "Armenia",
                    "Azerbaijan",
                    "Kyrgyzstan"
                ],
                "language": ["English"],
                "region": [""],
                "reportType": ["Rating Action Commentary", "Rating Action Report"],
                "sector": [
                    "US Public Finance",
                    "Supranationals, Subnationals, and Agencies",
                    "Sovereigns",
                    "International Public Finance"
                ]
            },
            "sort": "",
            "dateRange": "",
            "offset": 0,
            "limit": 24
        }
    })

    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'origin': 'https://www.fitchratings.com',
        'referer': 'https://www.fitchratings.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code != 200:
            return {"error": f"Failed to fetch data. HTTP Status Code: {response.status_code}"}

        data = response.json()
        search_results = data.get('data', {}).get('search', {})

        results = []

        for article_type, base_url, content_func in [
            ("racs", "https://www.fitchratings.com/research/", fitch_racs_content),
            ("research", "https://www.fitchratings.com/research/", fitch_reporturl_content)
        ]:
            articles = search_results.get(article_type, [])
            for article in articles:
                title = article.get('title')
                permalink = article.get('permalink')
                published_date = article.get('publishedDate', "").split("T")[0]

                raw_content = content_func(permalink) if permalink else ""
                clean_content = clean_html_content(raw_content)

                article_data = {
                    'title': title,
                    'date': published_date,
                    'content': clean_content,
                    'link': f"{base_url}{permalink}" if permalink else None,
                    'source': 'Fitch',
                    'keywords': None,
                    'region': 'CentralAsia',
                    'sector': 'sovereignsRACS'
                }
                save_article(article_data)
                results.append(article_data)

        return results

    except requests.RequestException as e:
        return {"error": f"Request failed: {e}"}

    except (json.JSONDecodeError, KeyError) as e:
        return {"error": f"Failed to parse response: {e}"}