import feedparser
import requests
from bs4 import BeautifulSoup
from utils.db_utils import save_article


def mckinsey_articles():
    rss_url = "https://www.mckinsey.com/insights/rss"

    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'OptanonAlertBoxClosed=2024-04-11T06:16:49.934Z; at_check=true; AMCVS_95851C8B53295A6D0A490D4D%40AdobeOrg=1; McKinseySessionID=104.109.251.46.13306631716990380939; shell#lang=en; _abck=38FD117C8AB086C741A9806C383E5ABC~0~YAAQBvttaCudPS+TAQAAGKlQPwz5gYqSz5455oTIVtl3asl0WcnH9ubCF8hfQcqWRObIHvZ/UVnXSVYbODkir9AYhGmFvNYQYfxzIurotcGTeoBqx3O7ee8oJ/d7TVtGL/H2KtW+I4MsMV/4lGDSV5h5teraFjo4j1ORiBTz8glrxxkzNWwmo15c5syAARhToslVUFjiq/3V/7DdvSzjSu8uvrbvqUySW/mrWrKT8I92BjNTXJroC34sf3nMzecPpDe5CG1Eb7WFOoq3TMoqDgZe1pdIiSLs8LZXqA5KXb7ghMbCMxo9VHeubHviHvmEvhc1pwc1P/8W94wL5sflL7uOMxIs32xPLN5PkPbDEs68sXgvSXgM3ZMonkwwhWK1Rlk5dfYA4jvtSSezCE8Ad8k4pyGeFhqDV3w=~-1~-1~-1; ak_bmsc=5487E3277C8B0F5D6B0543442DA8FC0B~000000000000000000000000000000~YAAQBvttaCydPS+TAQAAGKlQPxlAX/R21IN9hSGQS4ss2K0IURLpYlLPQBnCa1Ti69VAirM0YcP63DNM7YN+0lj6bvYW0RSIzNJIYqaPFbuSG2D19cw9sQY/wDLQKQ67e+KxJhvyOEsS0H48RtTuljcTRx9YkjbXoJaxw74EVOPezjLVeCrthWJ0pu2JiX47BrkyeYwG/N4g9mqZk33ni34rRrDIGS/A3MqtS52hl5zq9Wn33AZGQlBsuYEBGayWCh8LwvgVkNLe37hcegEXY4xu9UV7gEZhC1PyVFW971gI7fOn+Dwn5BYPnkNmQnL5qdXnxfQLMiD7BKcY63I48IOIc4MzlOvCs8hTmlo1jBgS1U89tf5510mcd1lijlm/4sCZoyZ6/ZaDhRg=; AKA_A2=A; bm_mi=1E1C51A65CDC5854F076778FD9B29C75~YAAQBvttaIytPi+TAQAALxxnPxkzejU9EGBdqzKGqZ7F6+QxDs6vp1QX14twjCCH/Qtd/7stzelBuwz8J+EozuAGc/wyW4l8XpCPb9qhkfTJ+8lniIKcOCiStamjD9PaEZzHIOnFi79y6cUIEfUKwMNcHICtLlw5DIm32p2F1cmkYTW7Ua1Kx4zFI8WJ2d/q9UQeCI0XMx4exu2mMaXx43NIROOj/nWtzl5RQ9zWJFTf5DM4+OGPZgJ9U4qie3NBgCk9EfU0hVtNek6tcR7wjvth6SBXuQLFcaVV7TRMHLUK4iZ0DvPoxHvZJToXGbIiFYFqzrlfFpBvhY5/laVU5u+q9KGeVLKpdZd+rSJqu6MGJMcP3IS2iThnLkr69PHtztgjpZ61ymvkRcTwdyHc2qgziW8RkgQ1Bpe5~1; bm_sv=06FF88BFFB308C96B4CD7FB794F7FC2E~YAAQBvttaHWvPi+TAQAAh0JnPxlw2IX4idWZaDAxvcZKBUyXZqRxQrYaa6+Quh0ReBdGwXWXRbsU0ppZuupXt5idptX99MuUehMa/dquEqvFQD25JbGBVScAjHtWlEJWjfzN0e94nf0UGM6tjcD8ZyFsBVGww6cXkoMF5Yg17BcBIjs3rJ96n6gqfG6p6Gl47d3bjaVNisxlK8OfOwcqpR2derbYE6C+56XmW73r1YtQwaRLCyMYxwT9C9dYyO1+bhw=~1; bm_sz=15EBC0784605336ADA5C922D255CB54E~YAAQBvttaHavPi+TAQAAh0JnPxkMmIEpQYcaquPVU4nlp/94VSQfGhKFNWjn0F7Mh1kI6NEIxCMKHGduxs+tMjbSBwb+TQEOcVza0FhdWThHiyt6ZEb2xAJb54EdRtLYLNc7L4Ph6yxr97iK7iofOUbwJYyEJLh3Z40YEYdUk5AwDJIRPyRZCdJly/23SoWJaaUf12LOuLY8MjJ6RT0Gmu5y8Ty1zVt3Nr8PIfHyyLfjdlbYjRl2lDJNsya0MmWjpbIbclxgThNmuAvDLLqvksHiQXaCFaBkJBOp62Vky+zDlhyIjDEnAp85eYv8ywfHXu6kWLLILCYn+WfPpPqOrMhD0eVOzWCsUgk1EUyUeipudaBkwsrFSyBO4darOqGIRASGNfusee1Lap0PmPyxamiYT53lWOOZZL5r0aATN1eatu9OdQ==~4277317~4277816; AMCV_95851C8B53295A6D0A490D4D%40AdobeOrg=179643557%7CMCIDTS%7C20046%7CMCMID%7C35303311821059047299185106348826259952%7CMCOPTOUT-1731942750s%7CNONE%7CvVersion%7C5.5.0; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Nov+18+2024+17%3A12%3A30+GMT%2B0400+(Gulf+Standard+Time)&version=202302.1.0&isIABGlobal=false&hosts=&consentId=656e7e49-f835-4ed7-aeaa-e2fd7ee73af9&interactionCount=1&landingPath=NotLandingPage&groups=C0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0001%3A1&geolocation=AE%3BDU&AwaitingReconsent=false; mbox=PC#9874ecb501b149ddb49d4295c0025746.37_0#1795180351|session#7b5aa5ee07e54cf0b4cc2cab9cdf0f44#1731935932; _abck=38FD117C8AB086C741A9806C383E5ABC~-1~YAAQtes/F/pFSTmTAQAAA91oPwyRcPkrv1Se7TJECgeiCdPW+sTg9cQGOJrXr4DBsjAvj6+HlP6VgOC8NAuTGaUGABn0ucnAyLduJRyKcbcLZqwF2n10X+PEe+fRas6TrWh8/Gup6i5F/pwKZBUvK6EQ2fUdsHg1TdIMLDl5lsix4C9M8tltwHi1A2p2xb3Nhk8CfLLO7UIvDK1mtV+3bM1k01qfaIXg05TYJQx2hNXOuXO4rcn0o1a72nTOyUN7HkAqNrp7QwLqDVjo29Me8LhQ2/HcUjHibC4JTSYcHPHCPF2nUqQP4CeNL2+c/FE9g49TpBL1s7tgGSJrmBV2MUlxTEEmoKHHxYSSSAWogM9QFeoEPsrwVcX+CC8BRJKYY+07xUzR3teko9plGNMox37DNoPXzVMhto8=~0~-1~-1; bm_mi=1E1C51A65CDC5854F076778FD9B29C75~YAAQtes/F/tFSTmTAQAAA91oPxmA2h595aMS321cAkQXVHa2yUGvDIn7VPFjq4WEoHDy0Eh41/vYtDDpt2ilqLLX/mbQ3S8xh8Dn0JuCWcEYOChKU2S7B5lrQTJXyTwieVtlxXp5Td9gJkKATAEXcMW0uuZYfdy3zaniOKjMZwb88gFZ3x43KeiuHH4Eb7Q+t77zm7TOipKTnjYLhOjeF9apopwBKFyj2UEz9gke5YTQ4Z47vIO5YdGd92AWI06F0wtPVExno7bIvBSGmGlyg5J8zrwALhTvBJowYxHTtI+ugG2vxYOXdc6C+P4wQGyPSD+d3zITFI800dkOA0JZSI5AzHAvYvYCdj2Q0WIYei1un+hM7inVTKfEI6L49WKycwJ+l72KNAGy7MgPGye9wSCco0PaTpNlBLyk~1; bm_sv=06FF88BFFB308C96B4CD7FB794F7FC2E~YAAQtes/F/xFSTmTAQAAA91oPxlmCJN71ObhUsGQgc16vRcgTyG4MhVUA1ceQyD8zTCp5xxIkoCgax+ciBPxSy/4ZYDyTUrZabqYunSs84EYU2podhAK/YVsZZG6dPLPb/T5A4W6xlvy7Oy/V5ddZ4jhJpUHjgeBv+NpnR+IUtxp3qZ2dYsyRl/7kdhvcfY28QaW4lDFOUaSz+7phscuDY3hnE3tFyEM8GHK9NYApoSW+Sj225gtHKweuB7huVLF8+U=~1; bm_sz=15EBC0784605336ADA5C922D255CB54E~YAAQtes/F/1FSTmTAQAAA91oPxlSisTxH4yG/ZL0GEgAhyCcSP752o+ReoERP+uUf9sWJjANcWjiwp33o1V53mE/047d3UOeIB1uaVDv9FEoWBhNWJaKqpEqjUHJhDvOMszdBoRqBjCpTmE3wciXjq7CM4M1Z2T5kGCE7v/6yaX3XynJXTdL3q1nFNQl1/Hq8cOCtXdoOiq0/+eJ7QCyLd7JQy/U1sPPJ5KviGvx7qvT0by/5KFVkTNjZI+XlzTXIPLWWVbOjkMBsfiXdDT6C728aPlb6VbVVpj35UWNc7FfJQHp+uZXTXM5pfgzGpJ8YMYYK1vFM0pcCqjkVsdmbw8i1X6yIhBCanHmSUzbssJ87mThXv3SK9cqyltFcIkPbs0b4zUWei1tcCJRI9nNnxlj9PLXwTLULMlzzyynRRImvJu8juPfb17qdVA=~4277317~4277816',
    'priority': 'u=0, i',
    'referer': 'https://www.mckinsey.com/insights/rss',
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
    if 'entries' in feed and len(feed.entries) > 0:
        articles = []
        for entry in feed.entries:
            title = entry.get('title', 'No title available')
            published_date = entry.get('published', 'No date available')
            link = entry.get('link', 'No link available')
            response = requests.get(link, headers=headers)
            if response.status_code == 200:
                html_content = response.content.decode('utf-8')
                soup = BeautifulSoup(html_content, 'html.parser')
                main_body = soup.find('main', {'data-layer-region': 'article-body'})
                if main_body:
                    paragraphs = main_body.find_all(['p', 'li'])
                    content = ' '.join([p.get_text(strip=True) for p in paragraphs])
                else:
                    content = 'No content available'

            article = {
                'title': title,
                'date': published_date,
                'summary': content,
                'url': link,
                'source': 'McKinsey',
                'keywords': None
            }
            save_article(article)
            articles.append(article)
        return articles