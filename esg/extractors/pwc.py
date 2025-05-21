import requests
import json
from datetime import datetime
from utils.db_utils import save_article
from utils.check import is_esg_related
import logging

def pwc_articles():
    url = "https://www.pwc.com/content/pwc/gx/en/research-insights/insights-library/jcr:content/root/container/content-free-container-1/section_2137231403/collection_v2.rebrand-filter-dynamic.html?currentPagePath=/content/pwc/gx/en/research-insights/insights-library&list=%7B%7D&searchText=&defaultImagePath=/content/dam/pwc/network/collection-fallback-images"

    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'JSESSIONID=node01q9scq1nfuwzf1614m9wfabs2k43430.node0; s_nr365=1713516338011-Repeat; at_check=true; ak_bmsc=3044D331EF819AD4FCF5E946277CC89D~000000000000000000000000000000~YAAQ5Z4QAtK1mCaTAQAAiIU4PxkEgxt1W/3yUHg2Uj79WwEZbcIW+sFvL1lSHd/nk6AIk4qvmR4mJb60pWhF/2R8hbL1wKbsFqXIJqZMXC84jbNrtJVi9Ud/lHSKoumIEQoF0jLbfPI71nRhEoSKQvZsK/4tX4ufEEq9q+qIb2vt/dEA6wr9hng4C56MVnZIOupEHC/YOWnMMMljeY7TqqW6NvLBI39F0OhLcVW77/Tilp2fvgR1DOzbLvs1ByOigNsls+y7i5Ao2RfoDWv2osv99I1mcPFG4uT+akru5lU7ZufjHqqBB/QTEUZtqd8KFPo6NB98HT98ngZo4cmHKMGDFH7xojv5yCGhBupbygNJkOJ7dlK3bizZdh6MJmWVGELTZZI1; mbox=session#60ea532283fe48fe84c9c82ac601e956#1731934368; bm_sv=B7DD81A2AD742813B96A6F1F25AAF33E~YAAQ5Z4QAo64mCaTAQAAY9k4Pxkgje10CBCfofSY9XRpcYqcnSkmyXvfOfqoeIVXf8BINiNwfZ98NxtOy8J8/0MOyerl8p/vS7if2ZMvqJ22zNb6u3McFiBnNbN6W46nBd02lNnHaSw9wTHaZ3bRKWK2ag0l4OM/DYwAnpm441v4RDnjbDD9wWv7rtFpwM1ObedD2gx3ju2UM8HjD87nSDgA79TCmzMuN2ZcEs3tYujJ2+usySui8gcFgBKN~1; bm_sv=B7DD81A2AD742813B96A6F1F25AAF33E~YAAQ5Z4QAn/jmCaTAQAA+vw8PxkLd5n1l4rcPf5BhBT91RM8kOKDCZu/wYrSaOovCJygDRNu0LVcJoHvfmOxbB8f9lGXHInTYI+07g1bx8z8e6b1NyNvMq8LZP5srpxK3J+3PGe7cHHrg56+0iC0iRq69qormwWpcpKd4BVeLYhDUy3iGn18G9OfTh/pgvfUuYCHtXVd5R+jeVVyiQR8HFUmdAYBaCdT0bHP78Uhqu/+oy2iIwiMWi1fc6gB~1',
    'priority': 'u=1, i',
    'referer': 'https://www.pwc.com/gx/en/research-insights/insights-library.html',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.get(url, headers=headers)
    articles = []
    if response.status_code == 200:
        data = json.loads(response.text)
        if 'elements' in data:
            articles_json = json.loads(data['elements'])
            for article in articles_json:
                title = article.get('title', 'No title available')
                href = article.get('href', 'No link available')
                publish_date = article.get('publishDate', 'No publish date available')
                text = article.get('text', 'No text available')
                try:
                    formatted_date = datetime.strptime(publish_date, "%B %d, %Y").strftime("%Y/%m/%d")
                except ValueError:
                    formatted_date = "Invalid date format"
                matched_keywords = is_esg_related(title, text)
                if not matched_keywords:
                    logging.debug(f"Skipping non-relevant article: {title}")
                    continue
                articles_data = {
                    'title': title,
                    'date': formatted_date,
                    'url': href,
                    'summary': text,
                    'source': 'PwC',
                    'keywords': matched_keywords
                }
                save_article(articles_data)
                articles.append(articles_data)
    return articles