import requests
from bs4 import BeautifulSoup
from dateutil import parser
import logging
from utils.check import is_ca_related
from utils.db import save_article

CORPORATE_KEYWORDS = [
    "Fitch Ratings","Moody's", "credit rating", "credit rating agency", "rating methodology",
    "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "credit rating scale",
    "investment grade", "speculative grade", "debt rating", "credit rating model", "credit rating criteria",
    "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review", "bond issuance",
    "sovereign bonds", "M&A", "credit risk", "assigns", "withdraws", "affirms", "upgrades", "downgrades", "guarantee", "guaranty", "guaranteed", "secured", "unsecured",

    "privatisation","corporate rating", "corporate bonds", "standalone credit profile", "issuer default rating", 
    "recovery rating", "recovery percentage", "government related entity", "corporate family rating", 

    "Uzbek geological exploration", "Uzbek geological", "Chimpharm", "Altynalmas", 
    
    "Navoi Mining and Metallurgical", "Navoi Mining and Metallurgy", "Navoiyuran", 
    "Almalyk Mining and Metallurgical", "Almalyk Mining and Metallurgy", "Almalyk MMC", 
    "Uzbek Metallurgical", "Uzbek Metallurgy", "Uzmetkombinat", "Uzbekneftegaz", "Uztransgaz", 
    "Hududgazta'minot", "Hududgaz", "UzGasTrade", "National Electric Grid of Uzbekistan", 
    "National Electric Grids of Uzbekistan", "Thermal Power Plants", "Regional Electrical Power Networks", 
    "Uzbekgeofizika", "Uzkimyosanoat", "Navoiyazot", "Navoi-Azot", "Navoiazot", 
    "Uzbek Railways", "Oʻzbekiston temir yoʻllari", "O'zbekiston Temir Yollari", 
    "Uzbekiston Temir Yollari", "Ozbekiston Temir Yollari", "Uzbekistan Railways", 
    "Uzbekistan Airways", "Uzbekistan Airports", "Toshshahartransxizmat", "UzAuto", 
    "Uz Auto", "Uzautosanoat", "Uzauto-sanoat", "Uzbektelecom", "Uzbek telecom", 
    "Uztelecom", "O'zbekiston pochtasi", "UzPost", "Uzbekistan Post", "Uzbekcoal", 
    "Artel Electronics", "Dehkanabad Potash Plant", "Dekhkanabad plant of potassium", 
    "Toshkent Metallurgiya Zavodi", "Tashkent Metallurgical Plant", "Tashkent Metallurgy Plant", 
    "SamAuto", "Samarqand Avtomobil zavodi", "SamAvto", "Akfa Aluminium", "Enter Engineering", 
    "Saneg", "Sanoat Energetika Guruhi", "Fargonaazot", "Farg'onaazot", "Hududiy Elektr Tarmoqla", 
    "Uzsungwoo", "QuvasoyCement", "Quvasoy Cement", "Kuvasaycement", "POSCO International Textile", 
    "Promxim Impex", "Kazakhstan Housing Company", "Samruk-Energy", "Samruk-Energo", 
    "Samruk Energy", "Samruk Energo", "Ekibastuz GRES-1", "Ekibastuz GRES 1", 
    "Samruk-Kazyna Construction", "Samruk Kazyna Construction", "Kazpost", "QazPost", 
    "Kazakhtelecom", "Kcell", "Kazakhstan Electricity Grid Operating Company", "KEGOC", 
    "KazMunayGas", "KazTransOil", "Astana Gas", "Astanagas", "Astana-Gas", "QazaqGaz", 
    "Intergas Central Asia", "KazTransGas", "Kazatomprom", "Kazakhstan Temir Zholy", 
    "Qazaqstan Temır Joly", "Kaztemirtrans", "Tengizchevroil", "Eurasian Resources Group", 
    "BI Group", "Kazakhstan Utility Systems", "Mangistau Regional Electricity Network", 
    "Food Contract Corp", "Food Contract Corporation", "TransteleCom", "Kaz Minerals", 
    "Kazakhmys", "BI Development", "Alma Telecommunications", "Batys transit", 
    "KazMunaiGas", "Kaztemirtrans", "Integra Construction"
]

def davaktiv():
    url = "https://davaktiv.uz/en/news"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    response = requests.get(url, headers=headers, verify=False)

    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        news_section = soup.find("section", class_="pages")
        news_articles = []

        if news_section:
            news_items = news_section.find_all("div", class_="news-item")
            for item in news_items:
                link_tag = item.find("a")
                title = link_tag.get_text(strip=True) if link_tag else "No title"
                url = link_tag["href"] if link_tag and link_tag.has_attr("href") else "No URL"
                date_tag = item.find("span", class_="date")
                date = date_tag.get_text(strip=True) if date_tag else "No date"
                formatted_date = parser.parse(date).strftime('%Y-%m-%d')
                article_response = requests.get(url, headers=headers, verify=False)
                if article_response.status_code == 200:
                    article_soup = BeautifulSoup(article_response.text, "html.parser")
                    content_container = article_soup.find("div", class_="content")
                    if content_container:
                        paragraphs = content_container.find_all("p")
                        content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
                    else:
                        content = "No content found"
                matched_keywords = is_ca_related(title, content, CORPORATE_KEYWORDS)
                if not matched_keywords:
                    logging.debug(f"Skipping non-relevant article: {title}")
                    continue


                articles_data = ({
                    "title": title,
                    "link": url,
                    "date": formatted_date,
                    "content": content,
                    "source": "Davaktiv",
                    "keywords": matched_keywords,
                    "region": "CentralAsia",
                    "sector": "corporates"
                })
                save_article(articles_data)
                news_articles.append(articles_data)
    return news_articles