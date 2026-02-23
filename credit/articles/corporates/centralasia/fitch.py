import json
import requests
from utils.db import save_article

CORPORATE_KEYWORDS = [
    "Moody's", "credit rating", "credit rating agency", "rating methodology",
    "credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", "credit rating scale",
    "investment grade", "speculative grade", "debt rating", "credit rating model", "credit rating criteria",
    "issuer rating", "credit report", "rating upgrade", "rating downgrade", "rating watch", "credit rating review", "bond issuance",
    "sovereign bonds", "M&A", "credit risk", "assigns", "withdraws", "affirms", "upgrades", "downgrades", "guarantee", "guaranty", "guaranteed", "secured", "unsecured",

    "corporate rating", "corporate bonds", "standalone credit profile", "issuer default rating", 
    "recovery rating", "recovery percentage", "government related entity", "corporate family rating", 
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

def fitch_article_content(slug):
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

def cp_ca_fitch():
    url = "https://api.fitchratings.com/"
    payload = json.dumps({
    "query": "query Search($item: SearchItem, $term: String!, $filter: SearchFilterInput, $sort: String, $dateRange: String, $offset: Int, $limit: Int) { search( item: $item term: $term filter: $filter sort: $sort dateRange: $dateRange offset: $offset limit: $limit ) { totalResearchHits totalRacsHits totalEntityHits totalIssueHits totalVideoHits totalEventHits totalWebinarHits totalAudioHits totalPageHits totalHits audio { image { poster __typename } createdDate permalink title __typename } event { title permalink eventType locationName startDate endDate timeZone image { poster thumbnail __typename } __typename } webinar { title permalink eventType locationName startDate endDate timeZone image { poster thumbnail __typename } __typename } research { docType marketing { contentAccessType { name slug __typename } language { name slug __typename } analysts { firstName lastName role sequenceNumber type __typename } countries { name slug __typename } sectors { name slug __typename } __typename } title permalink abstract reportType publishedDate ratingOutlookCode ratingOutlook sectorOutlookCode sectorOutlook __typename } racs { docType marketing { contentAccessType { name slug __typename } language { name slug __typename } analysts { firstName lastName role sequenceNumber type __typename } countries { name slug __typename } sectors { name slug __typename } __typename } title permalink abstract reportType publishedDate __typename } entity { marketing { analysts { firstName lastName role sequenceNumber type __typename } countries { name slug __typename } sectors { name slug __typename } __typename } name ultimateParent ratings { orangeDisplay ratingCode ratingAlertCode ratingActionDescription ratingAlertDescription ratingTypeDescription ratingEffectiveDate correctionFlag ratingChangeDate __typename } permalink __typename } issue { permalink issue issueName issuer entityName debtLevel deal className subClass transaction { description id securityList { typeDescription __typename } __typename } ratingDate maturityDate cusip isin originalAmount currency couponRate subgroupName ratableTypeDescription commercialPaperType marketing { analysts { firstName lastName type sequenceNumber __typename } countries { name slug __typename } sectors { name slug __typename } __typename } ratings { orangeDisplay ratableName ratingActionDescription ratingAlertCode ratingAlertDescription ratingCode ratingEffectiveDate ratingLocalActionDescription ratingLocalValue ratingTypeDescription ratingTypeId recoveryEstimate recoveryRatingValue solicitFlag sortOrder filterRatingType filterNationalRatingType filterInvestmentGradeType correctionFlag ratingChangeDate __typename } __typename } video { image { poster __typename } createdDate permalink title __typename } page { title slug image { poster thumbnail __typename } __typename } totalHits __typename } }",
    "variables": {
        "item": "ALL",
        "term": "",
        "filter": {
        "country": [
            "",
        ],
        "language": [
            "English",
        ],
        "region": [
          "",
          "Eastern Europe, Caucasus and Central Asia"
        ],
        "reportType": [
            "Non-Rating Action Commentary",
            "Special Report",
            "Outlook Report",
            "Credit Comment",
            "Navigator Report",
            "New Issue Report",
            "Japan Timely Disclosure",
            "Presale Report",
            "Transition and Default Studies",
            "Sector Credit Factors",
            "Recovery Tool",
            "Representations and Warranties",
            "Rating Report",
            "Rating Criteria",
            "Profile Report"
        ],
        "sector": [
            "",
            "Autos",
            "Aviation",
            "Chemicals and Fertilizers",
            "Corporate Finance",
            "Corporate Finance: Leveraged Finance",
            "Corporate Finance: Middle Markets",
            "Energy and Natural Resources",
            "Gaming, Lodging, and Leisure",
            "Healthcare and Pharma",
            "Industrials and Transportation",
            "Metals and Mining",
            "Real Estate and Homebuilding",
            "Retail and Consumer",
            "Technology, Media, and Telecom",
            "Utilities and Power"
            "Structured Finance",
            "Structured Finance: ABS",
            "Structured Finance: CMBS",
            "Structured Finance: Covered Bonds",
            "Structured Finance: RMBS",
            "Supranationals, Subnationals, and Agencies", 
            "Structured Finance: Structured Credit",
        ],
        "topic": [
            ""
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
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.fitchratings.com',
    'priority': 'u=1, i',
    'referer': 'https://www.fitchratings.com/',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()
        research_articles = data['data']['search']['research']
        results = []
        for article in research_articles:
            title = article['title']
            permalink = article['permalink']
            published_date = article['publishedDate'].split("T")[0]
            article_url = "https://www.fitchratings.com/research/" + permalink
            content = fitch_article_content(permalink)
            article_data = {
                'title': title,
                'date': published_date,
                'content': content,
                'link': article_url,
                'source': 'Fitch',
                'keywords': None,
                'region': 'CentralAsia',
                'sector': 'corporates'
            }
            save_article(article_data)
            results.append(article_data)

    return results