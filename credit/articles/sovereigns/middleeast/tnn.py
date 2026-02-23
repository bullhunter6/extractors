import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import re

tnn_KEYWORDS = [
    "Fitch Ratings", "S&P Global", "Moody's", "credit rating", "credit rating agency", "rating methodology", "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "Credit rating scale", "investment grade", "speculative grade",
    "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review", "bond rating", "bond issuance", "sovereign bonds",
    "M&A","bank bonds", "global banks",
    "global banking","First Abu Dhabi Bank", "FAB", "Emirates NBD", "Central Bank of the UAE", "CBUAE", "Abu Dhabi Commercial Bank", "ADCB", "Dubai Islamic Bank", "DIB", "Mashreq Bank", "Mashreq", "Mashreqbank", "Abu Dhabi Islamic Bank", "ADIB", "HSBC Bank Middle East", "HSBC UAE",
    "Commercial Bank of Dubai", "CBD", "Emirates Islamic", "RAK Bank", "The National Bank of Ras Al Khaimah", "Sharjah Islamic Bank", "SIB", "National Bank of Fujairah", "NBF", "Citibank UAE", "Bank of Sharjah",
    "Ajman Bank", "Arab Bank for Investment and Foreign Trade", "Al Masraf", "Arab Bank UAE", "Commercial Bank International", "CBI", "United Arab Bank", "UAB", "Emirates Development Bank", "EDB", "National Bank of Umm Al Qaiwain",
    "NBQ", "Al Hilal Bank", "Wio Bank", "Invest Bank", "Arab Monetary Fund", "AMF", "Emirates Investment Bank", "Tamweel", "Finance House", "Arab Trade Financing Program", "Mashreq Al Islami", "Credit Europe Bank Dubai",
    "Orient Insurance", "Sukoon Insurance", "Abu Dhabi National Insurance Company", "ADNIC", "Islamic Arab Insurance Company", "SALAMA", "Al Ain Ahlia Insurance", "Emirates Insurance", "Al Wathba National Insurance", "Al Buhaira National Insurance",
    "Union Insurance", "National General Insurance", "NGI", "Al Dhafra Insurance", "Abu Dhabi National Takaful Company", "Dubai Islamic Insurance and Reinsurance Company", "AMAN", "Dubai National Insurance and Reinsurance", "DNIR",
    "Al-Sagr National Insurance", "Methaq Takaful Insurance", "RAK Insurance", "Dubai Insurance", "Saudi Central Bank", "SAMA", "Saudi National Bank", "SNB", "Al Rajhi Bank", "Riyad Bank", "Saudi Awwal Bank", "SAB", "Banque Saudi Fransi",
    "BSF", "Alinma Bank", "Arab National Bank", "ANB", "Bank Albilad", "Saudi Investment Bank", "SAIB", "Bank AlJazira", "BAJ", "Gulf International Bank", "GIB Saudi", "Islamic Development Bank", "IDB", "Arab Petroleum Investments Corporation",
    "APICORP", "Islamic Corporation for the Development of the Private Sector", "ICD", "Tamweel Aloula", "Al-Yusr Leasing and Financing", "Nayifat Finance", "The Arab Investment Company", "TAIC", "AJIL Financial Services",
    "International Islamic Trade Finance Corporation", "ITFC", "Morabaha Marina Financing", "Alraedah Finance", "Aljabr Finance", "Quara Finance", "Al-Amthal Finance", "Gulf Finance Company", "The Company for Insurance", "Bupa Arabia",
    "Al Rajhi Insurance", "Al Rajhi Cooperative Insurance", "Walaa Cooperative Insurance", "Walaa Insurance", "Arabian Shield Insurance", "MedGulf Cooperative", "MedGulf Insurance", "Gulf Insurance Group", "Saudi Re",
    "Allianz Saudi Fransi Insurance", "Saudi Cooperative Insurance", "Al-Etihad Cooperative", "Al-Etihad Insurance", "Arabia Insurance Cooperative", "Malath Insurance", "United Cooperative Assurance",
    "Islamic Corporation for the Insurance of Investment and Export Credit", "ICIEC", "Buruj Cooperative Insurance", "Chubb Arabia Insurance"
]

def is_related(title, summary):
    if isinstance(summary, list):
        summary = " ".join(summary)
    elif not isinstance(summary, str):
        summary = ""
    content = title.lower() + " " + summary.lower()
    keyword_mapping = {keyword.lower(): keyword for keyword in tnn_KEYWORDS}
    pattern = r'\b(?:' + '|'.join(re.escape(keyword.lower()) for keyword in tnn_KEYWORDS) + r')\b'
    matched_keywords_lower = re.findall(pattern, content)
    matched_keywords_original = sorted({keyword_mapping[kw] for kw in matched_keywords_lower})

    return matched_keywords_original

def tnn_article_content(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch the URL: {url}, Status Code: {response.status_code}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find("script", id="fusion-metadata", type="application/javascript")
    if not script_tag:
        print("Unable to find the script tag with article data.")
        return None
    try:
        raw_json = script_tag.string
        start_idx = raw_json.find("Fusion.globalContent=") + len("Fusion.globalContent=")
        end_idx = raw_json.find("};", start_idx) + 1
        article_data = eval(raw_json[start_idx:end_idx])
    except Exception as e:
        print(f"Error parsing JSON data: {e}")
        return None
    content_elements = article_data.get("content_elements", [])
    content_list = []
    for element in content_elements:
        if element.get("type") == "text":
            content_list.append(element.get("content", ""))
    article_content = "\n\n".join(content_list)

    return article_content

def tnn_articles():
    api_url = "https://www.thenationalnews.com/pf/api/v3/content/fetch/story-feed-sections?query=%7B%22feedOffset%22%3A0%2C%22feedSize%22%3A20%2C%22includeSections%22%3A%22%2Fnews%2Fgulf%22%7D&d=848&_website=the-national"
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
        return []

    data = response.json()
    articles = []

    content_elements = data.get("content_elements", [])
    for element in content_elements:
        title = element.get("headlines", {}).get("basic", "No Title Found")
        raw_date = element.get("display_date", "No Date Found")
        link = element.get("canonical_url", "")
        try:
            if raw_date.endswith("Z"):
                raw_date = raw_date.replace("Z", "+00:00")
            date = datetime.fromisoformat(raw_date).strftime("%Y-%m-%d")
        except ValueError:
            date = "Invalid Date Format"
        full_link = f"https://www.thenationalnews.com{link}" if link else "No Link Found"
        content = tnn_article_content(full_link)
        matched_keywords = is_related(title, content)
        if not matched_keywords:
            logging.debug(f"Skipping non-relevant article: {title}")
            continue
        articles_info = ({
            "title": title,
            "date": date,
            "link": full_link,
            "content": content,
            "source": "The National News",
            "keywords": matched_keywords,
            "region": "MiddleEast",
            "sector": "sovereigns"
        })
        articles.append(articles_info)

    return articles