import requests
from bs4 import BeautifulSoup
import logging
from utils.check import is_ca_related
from utils.db import save_article
from dateutil import parser
from datetime import datetime

KEYWORDS = [
    "Fitch Ratings", "S&P Global", "Moody's", "credit rating", "credit rating agency", "rating methodology", "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "Credit rating scale", "investment grade", "speculative grade",
    "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review", 
    
    "privatisation","bond issuance", "sovereign bonds", "M&A","financial institutions", "financial institution", "bank bonds", "global banks","development bank", "development banks","sukuk",
    "return on equity", "ROE", "ROA", "retun on assets","equity","UAE bank","UAE banks", "banking system", "Finance system", "Basel", "banking regulations","NPLs","Non-Performing", 
    "Non Performing", "NPAs", "credit risk", "reinsurance", "global banking", "insurance", "banking regulations","open banking", "financial centre","anti-money laundering","banks' assets",
    "financial market","financial markets","financial stability","financial sector","financial services","financial system","financial technology","fintech","financial inclusion","banking sector",

    "Ministry of Investments","Money Transfers","Asia-Invest Bank", "Asian Development Bank","Ministry of Economy","National Investment Fund",

    "CIS banks","National Bank of Foreign Economic Activity", "NBU", "National Bank",
    "Uzpromstroybank", "SQB", "Agrobank", "Asakabank", "Ipoteka Bank", "Kapitalbank", "Xalq Bank",
    "Qishloq Qurilish Bank", "Business Development Bank", "Hamkorbank", "Microcreditbank", "Ipak Yuli",
    "Ipak Yuli Bank", "Aloqabank","Aloqa bank", "Turonbank", "Orient Finans Bank", "Trustbank", "KDB Bank Uzbekistan",
    "KDB Bank", "Asia Alliance Bank", "Invest Finance Bank", "Davr Bank", "Ravnaq Bank", "Uzagroleasing",
    "Universal Bank", "Uzbek Leasing International", "Hi-Tech Bank", "Madad Invest Bank", "Uzagroexport Bank",
    "Ziraat Bank Uzbekistan", "Ziraat Bank", "Alfa Invest Insurance", "Euroasia Insurance", "Impex Insurance",
    "Ingo Uzbekistan Insurance", "Kafil-Sug'urta", "Mosaic", "My Insurance", "Uzbekinvest",
    "National Bank of Kazakhstan", "Halyk Bank", "Baiterek", "Kaspi.kz", "Kaspi",
    "Kaspi Bank", "Bank CenterCredit", "Development Bank of Kazakhstan", "Otbasy Bank", "ForteBank",
    "First Heartland Jusan Bank", "Eurasian Bank", "Freedom Bank Kazakhstan", "Bereke Bank", "Bank RBK",
    "Agrarian Credit Corporation", "Citibank Kazakhstan", "Altyn Bank (China CITIC)", "Altyn Bank",
    "Home Credit Bank", "KazAgroFinance", "Shinhan Bank Kazakhstan", "Nurbank", "Damu Fund",
    "AB Bank China Kazakhstan", "Qazaq Banki", "Industrial and Commercial Bank of China (Almaty)",
    "KMF Microfinance Organization", "Kazakhstan-Ziraat International Bank", "VTB Bank Kazakhstan",
    "Al Hilal Islamic Bank", "Tengri Bank", "AsiaCredit Bank", "Capital Bank Kazakhstan",
    "Eurasian Development Bank", "KazakhExport Insurance","banking","Freedom Bank","Uzbek Industrial and Construction Bank"
]

def get_content_uz(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=0, i",
        "referer": "https://www.uzdaily.uz/en/section/1/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        content_block = soup.find("div", class_="content_body")
        paragraphs = content_block.find_all("p")
        content = "\n".join([p.get_text(strip=True) for p in paragraphs])
        return content
    return ""

def bk_uzdaily():
    urls = [
        "https://www.uzdaily.uz/en/section/2/",
        "https://www.uzdaily.uz/en/section/3/",
    ]

    headers = {
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    articles = []
    for url in urls:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            content_blocks = soup.find_all("a", class_="item_news_block")

            for block in content_blocks:
                link = block.get("href")
                if link:
                    full_link = f"https://www.uzdaily.uz{link}"
                else:
                    full_link = None
                date_span = block.find("span", class_="date")
                date = date_span.get_text(strip=True) if date_span else None
                parsed_date = datetime.strptime(date, "%d/%m/%Y")

                formatted_date = parsed_date.strftime("%Y-%m-%d")
                title_span = block.find("span", class_="name")
                title = title_span.get_text(strip=True) if title_span else None
                content = get_content_uz(full_link)
                matched_keywords = is_ca_related(title, content, KEYWORDS)
                if not matched_keywords:
                    logging.debug(f"Skipping non-relevant article: {title}")
                    continue
                articles_info = ({
                    "title": title,
                    "date": formatted_date,
                    "link": full_link,
                    "content": content,
                    "keywords": matched_keywords,
                    "source": "UzDaily",
                    "region": "CentralAsia",
                    "sector": "banks"
                })
                save_article(articles_info)
                articles.append(articles_info)
    return articles