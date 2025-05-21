import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from utils.db_utils import save_article

def cdp_articles():
    url = "https://www.cdp.net/en?filters%5Blocales%5D%5B%5D=en&filters%5Bprimary_topics%5D=all&filters%5Bsecondary_topics%5D=all&filters%5Btypes%5D%5B%5D=Cms%3A%3AArticle&filters%5Btypes%5D%5B%5D=Cms%3A%3APressRelease&page=3"

    headers = {
        'accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'locale=en; OptanonConsentFixClearedValues=true; OptanonConsentFixTriggered=true; OptanonAlertBoxClosed=2024-06-11T05:20:28.948Z; regional_selection_modal_choice_made=true; default_site_id=1; location=GLOB; detected_geographical_data_confirmed=true; cf_clearance=xUmWCvk_wzJEsYxlLceBYQZucLBm_.8fTk3_HFB7dGk-1727334161-1.2.1.1-3M6JKarmiWJv1dGR_1gKaZHKOT7e5eJundIxfVyu9.rg.N5sEGrCUPafE5EZ065fTrHQDlRMUnYmn1Dy313hzwCQjKE0C7Wi8zRbFfRGLhNvY8_uqPniWjoJ9_RV1mhBcSmO58Jeu3NV8_6CY46GkYdG81_IZBrC6nyy4p0zt1IS0_fgAy1csX3OW.6o7czzK.hV6GcPy0Wz0KZAQfTFMwGOrL92PFDB98LR_l63Po_Sjku1o078VxzyeOL28CfPzQ39vo2rwMNrcBpHvsH4U7H6.sozdh5ohaIj33_.HJnilWSAyOKINXuKzgcFQwvP1WOSoYRNTolSuM7GJQ9vdpRoralxjC73DXcw.qxuZlMUGaRiXWhqRA4bolNyYWcJt0d.aNmt1f6kzfCgr8b67w5l7M71XYWR.ok4psDW8Pk; session=80abb4b7e802c966163b3b10f9973dfb; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Nov+13+2024+10%3A04%3A05+GMT%2B0400+(Gulf+Standard+Time)&version=202409.2.0&isIABGlobal=false&hosts=H5%3A1%2CH6%3A1%2CH9%3A1%2CH16%3A0%2CH4%3A0%2CH15%3A0%2CH11%3A0%2CH14%3A0%2CH13%3A0%2CH12%3A0%2CH7%3A0%2CH8%3A0%2CH20%3A0%2CH21%3A0%2CH24%3A0%2CH26%3A0%2CH10%3A0&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=AE%3BDU&AwaitingReconsent=false&browserGpcFlag=0&genVendors=; locale=en; session=80abb4b7e802c966163b3b10f9973dfb',
        'priority': 'u=1, i',
        'referer': 'https://www.cdp.net/en/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"130.0.6723.117"',
        'sec-ch-ua-full-version-list': '"Chromium";v="130.0.6723.117", "Google Chrome";v="130.0.6723.117", "Not?A_Brand";v="99.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-csrf-token': 'hBBA4nQVawyRw01LMhzJYBQXXiyIp-pMqwX_u_R15ibllSsVdvrr41wtqDXOtAnka86Njip8-ogx02YCjPuYVA',
        'x-newrelic-id': 'XQAHVlFRGwYHUVVVBAg=',
        'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for post in soup.find_all("li", class_="st_channel__post"):
        link_tag = post.find("a", class_="article ga-track-newsfeed-cta")
        link = link_tag['href'] if link_tag else None

        title_tag = post.find("div", class_="article__title")
        title = title_tag.get_text(strip=True) if title_tag else "No title"

        type_date_tag = post.find("div", class_="article__type")
        type_date_text = type_date_tag.get_text(strip=True) if type_date_tag else "No type/date"
        
        date_match = re.search(r'\b\w+ \d{2} \d{4}\b', type_date_text)
        if date_match:
            date_str = date_match.group()
            date = datetime.strptime(date_str, "%B %d %Y").strftime("%Y-%m-%d")
        else:
            date = "No date"

        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find("div", class_="article__content")
        if content_div:
            summary = []
            for element in content_div.find_all(['p', 'li']):
                text = element.get_text(strip=True)
                if text:
                    summary.append(text)

        articles_data = {
            "title": title,
            "url": link,
            "date": date,
            "summary": summary,
            "source": "CDP",
            "keywords": "No Keywords"
        }
        save_article(articles_data)
        articles.append(articles_data)
    return articles