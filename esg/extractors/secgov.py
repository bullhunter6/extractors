import feedparser
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from utils.check import is_esg_related
import logging
from utils.db_utils import save_article

def secgov_articles():
    rss_url = "https://www.sec.gov/news/pressreleases.rss"

    headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-US,en;q=0.9',
      'cache-control': 'max-age=0',
      'cookie': 'ak_bmsc=AA67D2BB3577F462FB84F3F194BCF525~000000000000000000000000000000~YAAQt16MT/HCNCWTAQAAF/O2KRn+7JC0Krxl+3wnoO9tg7fCEqCzMdIZK3wrSi4TU+CbvVpgjawgRyzAAPMVXb2zwCai7sdpbf/LajEJPdESJ2z/EnCsmifPd3mhbsly2L6RQ+czlIA5hDi2TTeLwc9odamXn1XiM7QBhIoPFZAOi/H8w9dgd2GJm0viZIWEYNHIMKIRLXXB+FiEAMkYk6MCI4rIqrauHBrpV49ieQ5Oj1PV34XcrHSjl4jM/zmMh3vdSOmiAx1AEcxRc3FIEoZEhsh+ykLvmiwo1rn88a1/Z5GFm1RzO11fhzt5cO2JudA5b6dO4olXoOR15GASwSBw3iSB6KyQuG/8gfhwqixdteIZwz3Mj/we+b3Wx72g1Iv6FAu6; bm_mi=0D005A52E4FC9D6DD8B0A602651FFEDF~YAAQt16MT/bCNCWTAQAAN/S2KRkQ8jwdhcmpgbxAa99iDpzg2FUwe4OG2O6wWvhTo1psvvaWlKFbhC4mzU6G9v/F07hkTQPs8UJXBmRSw3tQ0/phB8NTQtogrkmMvpEhwcylrsmM0G24bRosoUCZ5HBwRFLhmlYVPScPB3GaR5UnCv3xumnqMCWRQ65QmUcgG8ArRe6tT0umIJBSvSMag0ZjefRjCOI+DawcRPWVbAUG/ZnRvdNNTggw24t9a0AO329gtJLihAlFuLHcPkQHQ6XeNr8T0j7NFCeZfjOWMI6pQGNdbY817tQYHOGahKV38NN2+uXBKsheMrm+zSSsxu0=~1; bm_sv=B95C835B9B3B0286E245989151DCC5E0~YAAQt16MT0rDNCWTAQAAzwW3KRme3Flg95otkKPcgo6broS1P8b2bIhpSXV3UL6w5dzH1NkLhuHMWwbgUgI8gJHSbRUI0/w/h1Xxo4oHWu6A2GqxPYXpnqZTTBnyj0GXn0m+SS1vqpOY4UZgZ33DLFaiDiE374UGVVNtWC7uwY5X+kCW/o/ysjn0jWdJsQK8meUzP2hwp5l8iKSTXcrgrzGBR0w5lcarOXg/v4HpyzBgAD9dnWXTZs/Oq7Gb~1; bm_mi=0D005A52E4FC9D6DD8B0A602651FFEDF~YAAQt16MT/HDNCWTAQAADle3KRlA3OPOUVjMAQij8sxY23LUNAvR91upgTwPDA/QaY1oFVigasx2uuql2zI9X/R3o7sZHxbSn/L5lcr2ZJ3YQB7VSMIxFR611a9mAzOhN3FWfsiRZ1YfvCXH5AN2bdIjjWh5B6NaW18c29FKzh44OR90AR/GRneKzWL9U3CRD2iHMUcOGzut3YpIo1WrTxjLm3xnjWiHXl0SuD/rXs5Lc9pLUigr7GT1huFezIbG2tNk0RP4HTdmnCJnlfHbml/EJK3Si/342Ax7R0bIWXxHmzBX+ZMZv37PpjqbnTQAmwZEUssaXxCswgq4EdUiXSKlfrkc7y+iaP4=~1; bm_sv=B95C835B9B3B0286E245989151DCC5E0~YAAQt16MT/LDNCWTAQAADle3KRnScgEfyTdHQxKdphzXCQ3I2oT0J9bShobOre9VfO84jlwnJ9RnCGvgII6ecBzeWlUZl8dSaWJBtnPGoABRrA0BV2e4hEc2vTSe0yYdd8GFniiYYnGQVBM/Iynq57U0sJun87ygGoU3j1U0MGsm00Ni2+HvU/6QsiMPOjDxMj763k2TzU6wUtxB0K2Aedlkz2kkymhqBsE1dz5pCLeuF1AaZAVBisAHAV5G~1',
      'priority': 'u=0, i',
      'referer': 'https://www.sec.gov/newsroom/press-releases',
      'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }

    feed = feedparser.parse(rss_url)

    articles = []
    for entry in feed.entries:
        title = entry.title.strip() if 'title' in entry else "No title available"
        link = entry.link if 'link' in entry else "No link available"
        description = entry.description.strip() if 'description' in entry else "No description available"
        pub_date = entry.published if 'published' in entry else "No date available"
        if pub_date:
            try:
                pub_date = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d')
            except ValueError:
                pub_date = "Invalid date format"
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        content_containers = [
            "node-details-layout__main-region__content",  
            "field--name-body",                           
            "clearfix text-formatted usa-prose"          
        ]
        content_paragraphs = []
        for container_class in content_containers:
            content_section = soup.find("div", class_=container_class)
            if content_section:
                content_paragraphs = content_section.find_all("p")
                if content_paragraphs:
                    break
        article_content = "\n\n".join([p.get_text(strip=True) for p in content_paragraphs]) if content_paragraphs else "No content found"
        matched_keywords = is_esg_related(title, article_content)
        if not matched_keywords:
            logging.debug(f"Skipping non-relevant article: {title}")
            continue

        article_data = {
            "title": title,
            "url": link,
            "date": pub_date,
            "description": article_content,
            "source": "SEC",
            "keywords": matched_keywords
        }
        save_article(article_data)
        articles.append(article_data)
    
    return articles
