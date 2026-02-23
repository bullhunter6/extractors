import requests
import json
from utils.check import filter_articles_by_region_2
from utils.keywords import COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS
from bs4 import BeautifulSoup
from utils.db import save_article


def kpmg():
    url = "https://kpmg.com/ecsearch/xx_en"

    payload = json.dumps({
      "id": "listing_industry_aggregation_template",
      "params": {
        "from": 0,
        "size": 15,
        "document_type": "INSIGHT",
        "sort": "desc",
        "industry_ids": [
          "149966161510941564767001",
          "192039136753087269580494",
          "131623764919550369614492",
          "110566678028133689052285",
          "190723427933480677659292"
        ]
      }
    })

    headers = {
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/json',
      'cookie': 'visit_settings=%7B%22count%22%3A3%2C%22mins%22%3A30%2C%22days%22%3A14%7D; sat_track=true; gig_bootstrap_3_e2ggAN5_ZqWrSNeM0HSHMYT8P16JqxINgs88bIrpCmPIiLJZ4zOqT69Wy7I6UByO=login_ver4; gig_bootstrap_3_eYey6Z79si-eeXEPJdZ-nHmhuCW-jna6Vvc90U_rCKgSJBvRulOycPAZkI--y8OB=login_ver4; affinity="322b0ae470ed0d0d"; gig_bootstrap_4_F4-OUyiGMyMU1r-H7Y8TSg=login_ver4; AMCVS_00B621ED542E84FD0A4C98A1%40AdobeOrg=1; gig_bootstrap_4_azL3BNfXLB_XWsTbbzd9Vw=login_ver4; AMCV_00B621ED542E84FD0A4C98A1%40AdobeOrg=179643557%7CMCIDTS%7C20062%7CMCMID%7C34031885092048535389020993488738769223%7CMCOPTOUT-1733321614s%7CNONE%7CvVersion%7C5.5.0',
      'origin': 'https://kpmg.com',
      'priority': 'u=1, i',
      'referer': 'https://kpmg.com/xx/en/our-insights.html',
      'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()
        hits = data.get("hits", {}).get("hits", [])
        articles = []
        for hit in hits:
            source = hit.get("_source", {})
            title = source.get("title")

            link = source.get("qualified_url")
            date = source.get("filter_date")
            
            content = "" # Initialize content
            try:
                response = requests.request("GET", link)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_div = soup.find('div', class_='section container responsivegrid')
                    if article_div:
                        headers = article_div.find_all('h5')
                        paragraphs = article_div.find_all('p')
                        content = '\n\n'.join(
                            tag.get_text(strip=True) for tag in (headers + paragraphs)
                        )
                    else:
                        print(f"DEBUG: No article content found for {link}")
                else:
                    print(f"DEBUG: Failed to fetch article {link} - Status: {response.status_code}")
            except Exception as e:
                print(f"DEBUG: Error fetching {link}: {e}")

            if content:
                region, keywords = filter_articles_by_region_2(title, content, COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS)
                if keywords:
                    print(f"DEBUG: Kept '{title}' - Region: {region}")
                    articles_info = ({
                        "title": title,
                        "link": link,
                        "date": date,
                        "content": content,
                        "region": region,
                        "keywords": keywords,
                        "source": "KPMG",
                        "sector": "banks"
                    })
                    save_article(articles_info)
                    articles.append(articles_info)
                else:
                    print(f"DEBUG: Skipped '{title}' - No matching keywords/region.")
            else:
                print(f"DEBUG: Skipped '{title}' - No content extracted.")

    return articles