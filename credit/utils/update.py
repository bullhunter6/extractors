import requests
import json
import pandas as pd

def get_slug(company_name: str) -> dict:
    url = "https://api.fitchratings.com/"
    payload = json.dumps({
        "query": """query Suggest($item: SearchItem, $term: String!) {
          suggest(item: $item, term: $term) {
            entity {
              name
              permalink
            }
          }
        }""",
        "variables": {
            "item": "ENTITY",
            "term": company_name
        }
    })
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.fitchratings.com',
        'priority': 'u=1, i',
        'referer': 'https://www.fitchratings.com/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Cookie': 'SSID_P=CQD5_B1GAAQAAACgzzlm4GeAA6DPOWYXAAAAAAAAAAAA57BFZwC3344AAAF1FAAA57BFZwEAkgAAA0UVAABxFSNnAgCLAAAByhMAAOewRWcBACoAAAELBQAA57BFZwEAeAAAAR0RAADnsEVnAQB0AAAA; SSOD_P=ABG_AAAAEgC6AAAAEQAAAKDPOWYRJVhmAAAAAA; SSRT_P=cLlFZwADAA; SSSC_P=1.G7366146951701620704.23|42.1291:120.4381:139.5066:142.5237:146.5445'
        }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code != 200:
        return None
    data = response.json().get("data", {}).get("suggest", {}).get("entity", [])
    for entity in data:
        if company_name.lower() in entity["name"].lower():
            return {"name": entity["name"], "permalink": entity["permalink"]}
    return None

def get_first_rating(permalink):
    url = "https://api.fitchratings.com/"
    payload = json.dumps({
        "query": """
            query Entity($slug: String!) {
                getEntity(slug: $slug) {
                    ratings {
                        id
                        orangeDisplay
                        correctionFlag
                        ratingChangeDate
                        ratingActionDescription
                        ratingCode
                        ratingAlertCode
                        ratingEffectiveDate
                        ratingTypeDescription
                        ratingLocalValue
                        ratingLocalActionDescription
                        recoveryRatingValue
                        __typename
                    }
                }
            }
        """,
        "variables": {"slug": permalink}
    })
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.fitchratings.com',
    'priority': 'u=1, i',
    'referer': 'https://www.fitchratings.com/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Cookie': 'SSID_P=CQD5_B1GAAQAAACgzzlm4GeAA6DPOWYXAAAAAAAAAAAA57BFZwC3344AAAF1FAAA57BFZwEAkgAAA0UVAABxFSNnAgCLAAAByhMAAOewRWcBACoAAAELBQAA57BFZwEAeAAAAR0RAADnsEVnAQB0AAAA; SSOD_P=ABG_AAAAEgC6AAAAEQAAAKDPOWYRJVhmAAAAAA; SSRT_P=cLlFZwADAA; SSSC_P=1.G7366146951701620704.23|42.1291:120.4381:139.5066:142.5237:146.5445'
    }
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        data = response.json()
        ratings = data.get("data", {}).get("getEntity", {}).get("ratings", [])
        if ratings:
            return ratings[0]
        else:
            return None
    
    return None

def process_companies(file_content):
    df = pd.read_excel(file_content)
    results = []
    
    for _, row in df.iterrows():
        company_name = row['Company Name']
        print(f"Processing {company_name}")
        company_details = get_slug(company_name)
        
        if company_details:
            first_rating = get_first_rating(company_details["permalink"])
            results.append({
                "Company Name": company_details["name"],
                "Entered Company Name": company_name,
                "Rating Code": first_rating.get("ratingCode") if first_rating else '-',
                "Outlook": first_rating.get("ratingAlertCode") if first_rating else '-',
                "Rating Type Description": first_rating.get("ratingTypeDescription") if first_rating else '-',
                "Rating Effective Date": first_rating.get("ratingEffectiveDate") if first_rating else '-',
                "Rating Action Description": first_rating.get("ratingActionDescription") if first_rating else '-'
            })
        else:
            results.append({
                "Company Name": company_name,
                "Entered Company Name": company_name,
                "Rating Code": '-',
                "Outlook": '-',
                "Rating Type Description": '-',
                "Rating Effective Date": '-',
                "Rating Action Description": '-'
            })
    results_df = pd.DataFrame(results)
    return results_df