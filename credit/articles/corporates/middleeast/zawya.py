import requests
import json
from utils.check import me_related
from utils.db import save_article
import logging

KEYWORDS = [
    "Fitch Ratings","Moody's", "credit rating", "credit rating agency", "rating methodology","credit score", "bond rating", "sovereign rating", "default risk", "rating outlook", 
    "credit rating scale", "investment grade", "speculative grade", "debt rating", "credit rating model", "credit rating criteria", "issuer rating", "credit report", "rating upgrade", 
    "rating downgrade", "rating watch", "credit rating review", "bond issuance","sovereign bonds", "M&A", "credit risk", "assigns", "withdraws", "affirms", "upgrades", "downgrades", 
    "guarantee", "guaranty", "guaranteed", "secured", "unsecured",

     "corporate issuance","corporate issuances","corporate rating", "corporate bonds", "standalone credit profile", "issuer default rating", "recovery rating", "recovery percentage", "government related entity", 
    "corporate family rating", "debt capital market", "corporate sukuk", "Sukuk issuance", "bond issuances", "green bonds", "sukuk", "sukuk issuance", "sukuk market",
    
    "Abu Dhabi National Energy Company", "TAQA", "National Central Cooling", 
    "Vista Global Holding", "ABU DHABI FUTURE ENERGY COMPANY", "Masdar", "DP WORLD", "Shelf Drilling Holdings", 
    "Fertiglobe", "Abu Dhabi Ports Company", "AD Ports Group", "Senaat", "EQUATE Sukuk", "Kuwait Projects", 
    "Damac", "Emaar", "Emirates Telecommunications Group Company", "Etisalat", "Aldar", "ADNOC", "Mamoura", 
    "Abu Dhabi Developmental Holding Company", "DUBAI AEROSPACE ENTERPRISE", "Majid Al Futtaim", "ACWA", 
    "EMIRATES SEMB CORP WATER AND POWER COMPANY", "EWEC", "Oztel", "RUWAIS", "SWEIHAN", "Abu Dhabi Crude Oil Pipeline", 
    "ADCOP", "Dae Funding", "Five Holdings", "Dubai Electricity and Water Authority", "DEWA", "Arada Developments", 
    "Ittihad International Investment", "DIFC Investments", "Emirates Strategic Investment Company", 
    "Private Department", "Taghleef Industries Holdco", "Taghleef Industries Topco", "Vantage Drilling International", 
    "Emirates Airline", "Telford Offshore", "Aerotranscargo FZE", "Brooge Petroleum and Gas Investment Company FZC", 
    "Telford Finco", "ACWA Power Capital Management", "2Rivers DMCC", "Eros Media World", "MRV Holding", 
    "Habtoor International", "A D N H Catering", "Abu Dhabi Aviation", "Abu Dhabi National for Building Materials", 
    "Abu Dhabi National Hotels", "Abu Dhabi National Oil Company For Distribution", "Abu Dhabi Ship Building", 
    "ADNOC Drilling Company", "ADNOC Gas", "ADNOC Logistics & Services", "Agility Global", "Agthia Group", 
    "Air Arabia", "AL KHALEEJ Investment", "Al Seer Marine Supplies & Equipment Company", "Alef Education Holding", 
    "Alpha Dhabi Holding", "Americana Restaurants International", "APEX INVESTMENT", "Aram Group", "Aramex", 
    "Borouge", "BURJEEL HOLDINGS", "Dana Gas", "Depa", "Deyaar Development", "Drake & Scull International", 
    "Dubai Investments", "Dubai Taxi Company", "E7 Group", "Easy Lease Motorcycle Rental", "Emaar Development", 
    "Emirates Central Cooling Systems Corporation", "Emirates Driving Company", "Emirates Integrated Telecommunications Company", 
    "Emirates Reem Investments", "EMSTEEL BUILDING MATERIALS", "ESG EMIRATES STALLIONS GROUP", "ESHRAQ INVESTMENTS", 
    "FOODCO NATIONAL FOODSTUFF", "Fujairah Building Industries", "Fujairah Cement Industries", "Ghitha Holding", 
    "Gulf Cement Co", "Gulf Medical Projects Company", "Gulf Navigation Holding", "Gulf Pharmaceutical Industries", 
    "HILY HOLDING", "International Holding Company", "Manazel", "MBME GROUP", "Modon Holding", "National Cement Co", 
    "National Corporation for Tourism & Hotels", "NATIONAL MARINE DREDGING COMPANY", "NMDC Energy", "Orascom Construction", 
    "PALMS SPORTS", "Parkin Company", "PHOENIX GROUP", "Presight AI Holding", "Pure Health Holding", "RAK Ceramics", 
    "RAK Properties", "Ras Al Khaimah Co for White Cement & Construction Materials", "Salik Company", 
    "Sharjah Cement and Industrial Development Company", "SPACE42", "Spinneys 1961 Holding", "Taaleem Holdings", 
    "Tecom Group", "Union Properties"
]

def zawya_business():
    url = "https://api.zawya.atexcloud.io/ace-pace-gateway/graphql"

    payload = "{\"query\":\"query readMore($path: String!, $siteId: ID!, $slotId: String!, $usedIds: [String!], $preview: String, $limit: Int, $offset: Int, $absolute: Boolean = false) @preview(data: $preview) {\\n  slot(path: $path, siteId: $siteId, slotId: $slotId, usedIds: $usedIds) {\\n    ... on Slot {\\n      ...SlotData\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment SlotData on Slot {\\n  id\\n  name\\n  headline\\n  headlineStyle\\n  colorScheme\\n  hidden\\n  link {\\n    ... on Link {\\n      hidden\\n      label\\n      url\\n      content {\\n        url\\n        path(absolute: $absolute)\\n        __typename\\n      }\\n      __typename\\n    }\\n    ... on WebContent {\\n      url\\n      path(absolute: $absolute)\\n      __typename\\n    }\\n    __typename\\n  }\\n  layout\\n  style\\n  adPosition\\n  customHtmlFragmentDesktop\\n  customHtmlFragmentMobile\\n  image {\\n    baseUrl\\n    height\\n    width\\n    __typename\\n  }\\n  teasers(limit: $limit, offset: $offset) {\\n    totalCount\\n    teasers {\\n      ... on Teaser {\\n        id\\n        title\\n        disableFallback\\n        teaserOvertitle\\n        mediaPlayInline\\n        text\\n        longText\\n        byline\\n        media {\\n          ... on Audio {\\n            image {\\n              width\\n              height\\n              crops {\\n                ...Crop\\n                __typename\\n              }\\n              baseUrl\\n              description\\n              __typename\\n            }\\n            __typename\\n          }\\n          ... on Image {\\n            baseUrl\\n            description\\n            width\\n            height\\n            crops {\\n              ...Crop\\n              __typename\\n            }\\n            __typename\\n          }\\n          ... on ImageGallery {\\n            image {\\n              width\\n              height\\n              crops {\\n                ...Crop\\n                __typename\\n              }\\n              baseUrl\\n              description\\n              __typename\\n            }\\n            __typename\\n          }\\n          ... on Video {\\n            image {\\n              width\\n              height\\n              crops {\\n                ...Crop\\n                __typename\\n              }\\n              baseUrl\\n              description\\n              __typename\\n            }\\n            __typename\\n          }\\n          __typename\\n        }\\n        content {\\n          __typename\\n          ... on Audio {\\n            mediaUrl\\n            mediaId\\n            path(absolute: $absolute)\\n            image {\\n              width\\n              height\\n              baseUrl\\n              __typename\\n            }\\n            parent {\\n              title\\n              ... on Section {\\n                path(absolute: $absolute)\\n                __typename\\n              }\\n              __typename\\n            }\\n            __typename\\n          }\\n          ... on Video {\\n            mediaUrl\\n            mediaId\\n            path(absolute: $absolute)\\n            caption\\n            image {\\n              width\\n              height\\n              baseUrl\\n              __typename\\n            }\\n            parent {\\n              title\\n              ... on Section {\\n                path(absolute: $absolute)\\n                __typename\\n              }\\n              __typename\\n            }\\n            hideAuthor\\n            byline\\n            authors {\\n              name\\n              role\\n              imageUrl\\n              path(absolute: $absolute)\\n              __typename\\n            }\\n            __typename\\n          }\\n          ... on Link {\\n            url\\n            content {\\n              id\\n              url\\n              __typename\\n            }\\n            __typename\\n          }\\n          ... on Article {\\n            topMedia {\\n              __typename\\n              ... on Video {\\n                mediaId\\n                __typename\\n              }\\n            }\\n            path(absolute: $absolute)\\n            premiumType\\n            publishedDate\\n            hideAuthor\\n            byline\\n            articleType\\n            overTitle\\n            teaserOvertitle\\n            parent {\\n              title\\n              ... on Section {\\n                path(absolute: $absolute)\\n                __typename\\n              }\\n              __typename\\n            }\\n            authors {\\n              name\\n              role\\n              imageUrl\\n              path(absolute: $absolute)\\n              __typename\\n            }\\n            provider {\\n              name\\n              disclaimer\\n              active\\n              __typename\\n            }\\n            __typename\\n          }\\n          ... on ImageGallery {\\n            title\\n            caption\\n            path(absolute: $absolute)\\n            items {\\n              image {\\n                baseUrl\\n                description\\n                __typename\\n              }\\n              __typename\\n            }\\n            hideAuthor\\n            byline\\n            authors {\\n              name\\n              role\\n              imageUrl\\n              path(absolute: $absolute)\\n              __typename\\n            }\\n            __typename\\n          }\\n        }\\n        ...CustomerTeaser\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  ...CustomerSlot\\n}\\n\\nfragment CustomerSlot on Slot {\\n  image {\\n    ... on Image {\\n      baseUrl\\n      description\\n      width\\n      height\\n      crops {\\n        ...Crop\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  showReadMore\\n}\\n\\nfragment CustomerTeaser on Teaser {\\n  media {\\n    ... on Audio {\\n      image {\\n        descriptionArabic\\n        __typename\\n      }\\n      __typename\\n    }\\n    ... on Image {\\n      descriptionArabic\\n      __typename\\n    }\\n    ... on ImageGallery {\\n      image {\\n        baseUrl\\n        descriptionArabic\\n        __typename\\n      }\\n      __typename\\n    }\\n    ... on Video {\\n      image {\\n        descriptionArabic\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  content {\\n    ... on Article {\\n      primaryKeyword {\\n        name\\n        url\\n        __typename\\n      }\\n      __typename\\n    }\\n    ... on ImageGallery {\\n      captionArabic\\n      __typename\\n    }\\n    ... on Link {\\n      label\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment Crop on CropInfo {\\n  imageFormat {\\n    name\\n    aspectRatio {\\n      width\\n      height\\n      __typename\\n    }\\n    __typename\\n  }\\n  cropRectangle {\\n    x\\n    y\\n    width\\n    height\\n    __typename\\n  }\\n}\\n\",\"variables\":{\"siteId\":\"contentid/section.zawya.en.site\",\"offset\":0,\"limit\":24,\"path\":\"business/investment\",\"slotId\":\"contentid/OWYxNGNmMjMtM2Q4ZS00\",\"absolute\":true}}"
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.zawya.com',
    'priority': 'u=1, i',
    'referer': 'https://www.zawya.com/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()
        teasers = data.get("data", {}).get("slot", {}).get("teasers", {}).get("teasers", [])
        articles = []
        for teaser in teasers:
            title = teaser.get("title")
            date =  teaser.get("content", {}).get("publishedDate")
            link = teaser.get("content", {}).get("path")
            content = teaser.get("text")
            matched_keywords = me_related(title, content, KEYWORDS)
            if not matched_keywords:
                logging.debug(f"Skipping non-relevant article: {title}")
                continue
            articles_info = ({
                "title": title,
                "date": date,
                "link": link,
                "content": content,
                "source": "Zawya",
                "keywords": matched_keywords,
                "region": "MiddleEast",
                "sector": "corporates"
            })
            save_article(articles_info)
            articles.append(articles_info)
        return articles
    
def zawya_bonds():
    url = "https://api.zawya.atexcloud.io/ace-pace-gateway/graphql"

    payload = "{\"query\":\"query readMore($path: String!, $siteId: ID!, $slotId: String!, $usedIds: [String!], $preview: String, $limit: Int, $offset: Int, $absolute: Boolean = false) @preview(data: $preview) {\\n  slot(path: $path, siteId: $siteId, slotId: $slotId, usedIds: $usedIds) {\\n    ... on Slot {\\n      ...SlotData\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment SlotData on Slot {\\n  id\\n  name\\n  headline\\n  headlineStyle\\n  colorScheme\\n  hidden\\n  link {\\n    ... on Link {\\n      hidden\\n      label\\n      url\\n      content {\\n        url\\n        path(absolute: $absolute)\\n        __typename\\n      }\\n      __typename\\n    }\\n    ... on WebContent {\\n      url\\n      path(absolute: $absolute)\\n      __typename\\n    }\\n    __typename\\n  }\\n  layout\\n  style\\n  adPosition\\n  customHtmlFragmentDesktop\\n  customHtmlFragmentMobile\\n  image {\\n    baseUrl\\n    height\\n    width\\n    __typename\\n  }\\n  teasers(limit: $limit, offset: $offset) {\\n    totalCount\\n    teasers {\\n      ... on Teaser {\\n        id\\n        title\\n        disableFallback\\n        teaserOvertitle\\n        mediaPlayInline\\n        text\\n        longText\\n        byline\\n        media {\\n          ... on Audio {\\n            image {\\n              width\\n              height\\n              crops {\\n                ...Crop\\n                __typename\\n              }\\n              baseUrl\\n              description\\n              __typename\\n            }\\n            __typename\\n          }\\n          ... on Image {\\n            baseUrl\\n            description\\n            width\\n            height\\n            crops {\\n              ...Crop\\n              __typename\\n            }\\n            __typename\\n          }\\n          ... on ImageGallery {\\n            image {\\n              width\\n              height\\n              crops {\\n                ...Crop\\n                __typename\\n              }\\n              baseUrl\\n              description\\n              __typename\\n            }\\n            __typename\\n          }\\n          ... on Video {\\n            image {\\n              width\\n              height\\n              crops {\\n                ...Crop\\n                __typename\\n              }\\n              baseUrl\\n              description\\n              __typename\\n            }\\n            __typename\\n          }\\n          __typename\\n        }\\n        content {\\n          __typename\\n          ... on Audio {\\n            mediaUrl\\n            mediaId\\n            path(absolute: $absolute)\\n            image {\\n              width\\n              height\\n              baseUrl\\n              __typename\\n            }\\n            parent {\\n              title\\n              ... on Section {\\n                path(absolute: $absolute)\\n                __typename\\n              }\\n              __typename\\n            }\\n            __typename\\n          }\\n          ... on Video {\\n            mediaUrl\\n            mediaId\\n            path(absolute: $absolute)\\n            caption\\n            image {\\n              width\\n              height\\n              baseUrl\\n              __typename\\n            }\\n            parent {\\n              title\\n              ... on Section {\\n                path(absolute: $absolute)\\n                __typename\\n              }\\n              __typename\\n            }\\n            hideAuthor\\n            byline\\n            authors {\\n              name\\n              role\\n              imageUrl\\n              path(absolute: $absolute)\\n              __typename\\n            }\\n            __typename\\n          }\\n          ... on Link {\\n            url\\n            content {\\n              id\\n              url\\n              __typename\\n            }\\n            __typename\\n          }\\n          ... on Article {\\n            topMedia {\\n              __typename\\n              ... on Video {\\n                mediaId\\n                __typename\\n              }\\n            }\\n            path(absolute: $absolute)\\n            premiumType\\n            publishedDate\\n            hideAuthor\\n            byline\\n            articleType\\n            overTitle\\n            teaserOvertitle\\n            parent {\\n              title\\n              ... on Section {\\n                path(absolute: $absolute)\\n                __typename\\n              }\\n              __typename\\n            }\\n            authors {\\n              name\\n              role\\n              imageUrl\\n              path(absolute: $absolute)\\n              __typename\\n            }\\n            provider {\\n              name\\n              disclaimer\\n              active\\n              __typename\\n            }\\n            __typename\\n          }\\n          ... on ImageGallery {\\n            title\\n            caption\\n            path(absolute: $absolute)\\n            items {\\n              image {\\n                baseUrl\\n                description\\n                __typename\\n              }\\n              __typename\\n            }\\n            hideAuthor\\n            byline\\n            authors {\\n              name\\n              role\\n              imageUrl\\n              path(absolute: $absolute)\\n              __typename\\n            }\\n            __typename\\n          }\\n        }\\n        ...CustomerTeaser\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  ...CustomerSlot\\n}\\n\\nfragment CustomerSlot on Slot {\\n  image {\\n    ... on Image {\\n      baseUrl\\n      description\\n      width\\n      height\\n      crops {\\n        ...Crop\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  showReadMore\\n}\\n\\nfragment CustomerTeaser on Teaser {\\n  media {\\n    ... on Audio {\\n      image {\\n        descriptionArabic\\n        __typename\\n      }\\n      __typename\\n    }\\n    ... on Image {\\n      descriptionArabic\\n      __typename\\n    }\\n    ... on ImageGallery {\\n      image {\\n        baseUrl\\n        descriptionArabic\\n        __typename\\n      }\\n      __typename\\n    }\\n    ... on Video {\\n      image {\\n        descriptionArabic\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  content {\\n    ... on Article {\\n      primaryKeyword {\\n        name\\n        url\\n        __typename\\n      }\\n      __typename\\n    }\\n    ... on ImageGallery {\\n      captionArabic\\n      __typename\\n    }\\n    ... on Link {\\n      label\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment Crop on CropInfo {\\n  imageFormat {\\n    name\\n    aspectRatio {\\n      width\\n      height\\n      __typename\\n    }\\n    __typename\\n  }\\n  cropRectangle {\\n    x\\n    y\\n    width\\n    height\\n    __typename\\n  }\\n}\\n\",\"variables\":{\"siteId\":\"contentid/section.zawya.en.site\",\"offset\":0,\"limit\":24,\"path\":\"capital-markets/bonds\",\"slotId\":\"contentid/OWYxNGNmMjMtM2Q4ZS00\",\"absolute\":true}}"
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.zawya.com',
    'priority': 'u=1, i',
    'referer': 'https://www.zawya.com/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()
        teasers = data.get("data", {}).get("slot", {}).get("teasers", {}).get("teasers", [])
        articles = []
        for teaser in teasers:
            title = teaser.get("title")
            date =  teaser.get("content", {}).get("publishedDate")
            link = teaser.get("content", {}).get("path")
            content = teaser.get("text")
            matched_keywords = me_related(title, content, KEYWORDS)
            if not matched_keywords:
                logging.debug(f"Skipping non-relevant article: {title}")
                continue
            articles_info = ({
                "title": title,
                "date": date,
                "link": link,
                "content": content,
                "source": "Zawya",
                "keywords": matched_keywords,
                "region": "MiddleEast",
                "sector": "corporates"
            })
            save_article(articles_info)
            articles.append(articles_info)
        return articles

def zawya_cp():
    return zawya_business() + zawya_bonds()

