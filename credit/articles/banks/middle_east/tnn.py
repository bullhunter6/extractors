import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import re
import json

tnn_KEYWORDS = [
    "Fitch Ratings", "S&P Global", "Moody's", "credit rating", "credit rating agency", "rating methodology", "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "Credit rating scale", "investment grade", "speculative grade",
    "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review",
    
    "bond issuance", "sovereign bonds", "M&A","financial institutions", "financial institution", "bank bonds", "global banks","development bank", "development banks","sukuk",
    "return on equity", "ROE", "ROA", "retun on assets","equity","UAE bank","UAE banks", "banking system", "Finance system", "Basel", "banking regulations","NPLs","Non-Performing", 
    "Non Performing", "NPAs", "credit risk", "reinsurance", "global banking", "insurance sector","banking regulations","open banking", "financial centre","anti-money laundering","banks' assets",
    "tax","financial market","financial markets","financial stability","financial sector","financial services","financial system","financial technology","fintech","financial inclusion",

    "First Abu Dhabi Bank", "FAB", "Emirates NBD", "Central Bank of the UAE", "CBUAE", "Abu Dhabi Commercial Bank", "ADCB", "Dubai Islamic Bank", "DIB", "Mashreq Bank", "Mashreq", "Mashreqbank", "Abu Dhabi Islamic Bank", "ADIB", "HSBC Bank Middle East", "HSBC UAE",
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
    "Islamic Corporation for the Insurance of Investment and Export Credit", "ICIEC", "Buruj Cooperative Insurance", "Chubb Arabia Insurance","AAOIFI","World Bank"
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
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find article body in ld+json first as it's cleaner
        ld_json_scripts = soup.find_all("script", type="application/ld+json")
        for script in ld_json_scripts:
            try:
                if not script.string:
                    continue
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get("@type") == "NewsArticle":
                    body_html = data.get("articleBody", "")
                    if body_html:
                        body_soup = BeautifulSoup(body_html, 'html.parser')
                        return body_soup.get_text(separator="\n\n").strip()
            except:
                continue

        # Fallback to Fusion.globalContent if ld+json fails
        script_tag = soup.find("script", id="fusion-metadata", type="application/javascript")
        if script_tag and script_tag.string:
            match = re.search(r'Fusion\.globalContent\s*=\s*(\{.*?\});', script_tag.string)
            if match:
                try:
                    article_data = json.loads(match.group(1))
                    content_elements = article_data.get("content_elements", [])
                    content_list = []
                    for element in content_elements:
                        if element.get("type") == "text":
                            content_list.append(element.get("content", ""))
                    if content_list:
                        article_content = "\n\n".join(content_list)
                        return BeautifulSoup(article_content, 'html.parser').get_text(separator="\n\n").strip()
                except:
                    pass
    except Exception as e:
        logging.error(f"Error fetching article content: {e}")
    
    return None

def tnn_articles():
    section_url = "https://www.thenationalnews.com/news/gulf/"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(section_url, headers=headers, timeout=15)
        if response.status_code != 200:
            return []
        
        match = re.search(r'Fusion\.contentCache\s*=\s*(\{.*?\});', response.text, re.DOTALL)
        if not match:
            return []
            
        cache_data = json.loads(match.group(1))
        seen_urls = set()
        articles = []
        
        # Iterate through all keys in the cache to find article elements
        for key in cache_data:
            # Each key (like 'content-api-collections') contains a dict where keys are params and values are the data
            params_dict = cache_data[key]
            if not isinstance(params_dict, dict):
                continue
                
            for params_key in params_dict:
                data_container = params_dict[params_key]
                if not isinstance(data_container, dict):
                    continue
                    
                data_obj = data_container.get('data', {})
                if not isinstance(data_obj, dict):
                    continue
                    
                elements = data_obj.get('content_elements', [])
                if not isinstance(elements, list):
                    continue
                    
                for item in elements:
                    if not isinstance(item, dict):
                        continue
                    
                    # Extract title, url, and date
                    title = item.get('headlines', {}).get('basic') or item.get('headlines', {}).get('web')
                    url = item.get('website_url') or item.get('canonical_url')
                    raw_date = item.get('display_date') or item.get('publish_date') or item.get('last_updated_date')
                    
                    if title and url:
                        full_link = url if url.startswith('http') else f"https://www.thenationalnews.com{url}"
                        if full_link in seen_urls:
                            continue
                        seen_urls.add(full_link)
                        
                        # Process date
                        date = "Invalid Date"
                        if raw_date:
                            try:
                                if raw_date.endswith("Z"):
                                    raw_date = raw_date.replace("Z", "+00:00")
                                date = datetime.fromisoformat(raw_date).strftime("%Y-%m-%d")
                            except:
                                pass
                        
                        content = tnn_article_content(full_link)
                        if not content:
                            continue
                            
                        matched_keywords = is_related(title, content)
                        if not matched_keywords:
                            continue
                            
                        articles.append({
                            "title": title.strip(),
                            "date": date,
                            "link": full_link,
                            "content": content,
                            "source": "The National News",
                            "keywords": matched_keywords,
                            "region": "MiddleEast",
                            "sector": "banks"
                        })
                    
        return articles
        
    except Exception as e:
        logging.error(f"Error in tnn_articles: {e}")
        return []
