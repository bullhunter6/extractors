import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
from utils.check import filter_articles_by_region_2
from utils.keywords import COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS
from utils.db import save_article


def mck():
    url = "https://prd-api.mckinsey.com/api/insightsgrid/articles"

    payload = json.dumps({
      "limit": 11,
      "afterId": "",
      "taxonomyAndTags": {
        "taxonomyQueryType": "OR",
        "taxonomyIds": [
          "4d286384-e302-4ff6-882f-f43b94ec10a6",
          "f93af4d0-e649-48ff-9dbb-dd307c4a8c04",
          "be7f812a-bbfe-43b4-bdc0-9cc8fccdc5ec",
          "886d5eb0-3df8-4fe2-9d05-5d2fbdd30a05",
          "081c2023-9a21-40d5-b522-da25a4e1a6ed"
        ],
        "mustHaveTagsQueryType": "OR",
        "mustHaveTags": [
          "91cfe105-8dad-437c-8734-3d740dcdb437",
          "887e7cb2-191e-44d5-9ec6-de040b312a25",
          "a9103a6d-6663-4a30-bf78-9927d74f5df5",
          "fa4bb8d5-ea76-4dd9-9530-2c865a87d5e0",
          "45c4660b-c2d9-49c6-9536-c259c7e988d6",
          "83cf99bc-d256-4e4c-a1bf-d0698ec601e9",
          "21dc6bd4-9b9a-4de0-a9b8-71f68efef898",
          "874ee345-9fa7-403b-bcf3-2eaf719a89fa",
          "1ea27058-9b4d-4a64-81f4-f56cb6b81896",
          "aaf8b700-2f9c-40e9-8037-7a90ebf4e651",
          "c3f331dd-6683-4c33-9460-e56bb1487f33",
          "13f7e352-920f-4dd2-9a31-f2c3314eb405",
          "5b69151c-e124-4dcf-b9e7-212b7320050d"
        ],
        "mustNotHaveTagsQueryType": "OR",
        "mustNotHaveTags": [
          "a65a9603-c09a-489f-9d77-4afd71c629b3",
          "5ab0a0be-a65e-4648-bd51-f7a1a8850607"
        ]
      },
      "excludeItems": [
        "73b21cfb-e0c4-466b-958c-cb66bc262e71",
        "e9e5161c-a204-4f4f-956a-4d8a3c6dd690",
        "449f43bd-446a-41ed-abb6-39da72e97593",
        "fbfdf8a5-0c35-4b45-b0a4-992b68099ccc",
        "5c047528-bf04-44b3-984a-0e9befdee7cc",
        "3b96ae8c-23ff-4d47-8e2f-20cd3f92d612",
        "85475041-552c-441e-81e1-b50c10d5dccc",
        "59b1c531-bad3-425d-b787-3b470d5be81d",
        "d3d97da1-041a-493e-99c9-73b5bf875373",
        "deee0a7b-8a47-434f-aacd-56ca4a63a73b",
        "9215ffb0-a5ea-4e88-90c2-1937622fa852",
        "97a94f86-041b-463b-bc22-d5864f594175",
        "6064b039-8910-434b-9367-b56a8f740079",
        "0e36632a-d192-4ed6-ac7f-76dc04d100b5",
        "9e0160fe-e0b1-40ce-b872-411dff3123d0",
        "516c47d0-2b28-4dbe-a202-f7bf1d8baee9",
        "f2555791-3e1c-49c1-b80b-10407628d8d9",
        "396e3c3a-c008-4aca-9da7-b858761dbd1b",
        "53f8d0f8-4e11-4573-8f71-443d8e606f7d",
        "7c8ea494-a5f8-4cd5-b76e-98eaf8ab0677",
        "5b2196bd-6387-449b-b6c2-ff342129aa50",
        "c81573a2-787e-4100-b5ef-569625e63b57",
        "5f2d6c15-96e7-41f1-bc07-62440d9ed07f",
        "4bedbe51-7ec6-4704-adb3-857bd1fc1175",
        "df415f26-a046-45dd-9aee-41b7171a2aa2",
        "3ae0cadc-e292-4917-9505-d965edbcc292",
        "142de58a-d3ea-4e88-8d81-a22e6a1ebdfb",
        "9ee98f06-2e6b-4055-ac16-c3373418e063",
        "381d3c84-bed4-40d3-8565-53db6e082187",
        "a322bece-9af7-45e2-9646-cd0dc4848e7d",
        "785e3130-d36f-4395-94e4-54fa3739e171",
        "3f2f816c-9225-4e86-9bc8-af496eb9d031",
        "62d3701b-dc13-4038-81e4-1eecdeff49a1",
        "5708039b-6948-4c89-bf96-3726a08ec4b4",
        "b866e367-cfad-43e5-bd0f-95a43d4d0018",
        "d048f713-6c74-4cd5-8ff9-1e79d0644865",
        "9cc12254-8cf3-4d22-b896-c6b85ebb5fef",
        "daaa76e3-b16e-43c8-b7ee-3564a842b654",
        "6642642d-717c-4dec-b4d2-7879dd8ea529",
        "477e63ca-322a-481b-bf62-55e2491a19cc",
        "68747568-8444-4d4c-81f4-a038a5ba6172",
        "b8d31de4-4219-4967-b41b-0a03744070b5",
        "3966f681-6947-494b-82e7-24c94f5891c5",
        "4eba7fcf-cf42-49e4-96a6-0474cae904a4",
        "76997f5e-f16a-4eba-b92a-dedf0d4a30d5",
        "bc5b5382-cae7-428e-afbd-e1845a206106",
        "c553755e-a447-465a-bd17-cd008f7b42e6",
        "6e0dec43-2749-490a-acfa-5d83dd6f7c2b",
        "e2b47fd1-94f4-4872-9b92-9cc4bde9d21f",
        "c4abb92e-3603-4165-9093-cd9fcbbfbc27",
        "5749afab-df3c-48f7-9ea7-f7ec9d845d90",
        "72ece343-0ce8-4b51-ab31-7f61dc3e193a",
        "ded7990b-4807-4017-93dc-7ca994db6300",
        "140f5ecc-c78e-40a6-9da7-1bc3f8859788",
        "07b248e0-ed90-47f3-82fe-489b6fc258f9",
        "fcaa0afc-cd7e-479b-a0e7-918b4de87313",
        "a0376e1f-1456-4802-8be2-983c1a9f8f3f",
        "c63b8c1c-b052-4035-9b57-ccfa5714731c",
        "3e7e47d9-9258-4e13-a6d3-f4540e46dfd0",
        "3340e0b5-81c4-4e96-bdaf-7e933bac545a",
        "04fc435c-2614-4401-a9ed-e82efdb071fe",
        "2fb1e26b-0922-4132-8d3e-da1679527ac3",
        "a9907f93-c859-42b7-a34b-2bf1abb5e4dc",
        "880ed20f-f5e1-4ef3-b6b5-ad9dfaf1bf31",
        "5a65e540-6d39-4006-8ead-09e880c0450b",
        "1445e0d1-09ab-4e62-99c9-f2906255ef82",
        "7632c89e-11f4-4a78-82b4-951f2df0de77",
        "e27d90f1-efcf-40cd-bd0b-34edd1c755fe",
        "a80d6140-d20e-4d51-a461-94d569c3cf2a",
        "ce9c226f-9cf7-4d31-be0e-7fddded387f8",
        "ba4d0d65-b313-4c9a-9eb6-c31215e9274c",
        "60af1923-a1e6-4db2-8ee4-5b1e97ff94a8",
        "b92c4d2a-1035-4b4f-b0ee-50547fe460d7",
        "7e35096d-d144-4afb-b18e-cef6783bb014",
        "27cc7141-1a96-468a-9b8c-aae2b27f9b8f",
        "002d4515-2c1d-4e7e-91dc-2723bacc1194",
        "c7ebd27c-3938-4e63-9e18-aa9dd1179933",
        "cfb29bdf-c031-4e18-b275-62e1800a2299",
        "e980c69d-c09d-41be-a35d-c0766aea42ad",
        "ba1e1a8f-22cf-4654-90b2-13476f2f8df0",
        "8d8669c2-59b1-4a51-ba9b-4eee9d94eb8e",
        "76f1642f-566f-4e0d-917f-a60034800fe3",
        "074a33c3-74d7-46e2-a3d9-4fc326088c6c",
        "f898bab1-7caf-4de3-a5e4-76f3d4308178",
        "c39f26b9-d568-4e3d-bc74-f1474aaa86e9",
        "9996c5eb-66a7-49ef-8449-1c20e095c141",
        "946b1aea-d711-4db0-9139-89b2c478c2a3",
        "6ade1ffb-b818-446e-8058-2aae26cbd064",
        "9f899429-fb69-4519-aef5-7311c4c95e72",
        "9144cd13-6f84-47de-bc60-910e59565624",
        "d36f860b-f063-4550-8908-a1e16f90d8eb",
        "3cb5d295-e758-49bb-ae99-5a6beeb48d78",
        "53292844-58ba-4c65-a639-0932c61afc54",
        "b53cebcf-8bb7-4dcb-9ec5-2b90d64e8e60",
        "a31d576c-146b-4ae5-95ec-2aeb86032c42"
      ],
      "language": "en",
      "isAlumni": False,
      "filters": []
    })
    headers = {
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/json',
      'origin': 'https://www.mckinsey.com',
      'priority': 'u=1, i',
      'referer': 'https://www.mckinsey.com/industries/financial-services/our-insights',
      'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      'Cookie': '_abck=38FD117C8AB086C741A9806C383E5ABC~-1~YAAQBvttaBu05YKTAQAAyRigmw1KjQAhZuiIFEGzbc8XPlYiVWzHyTOmsNr/A9x6UhQXNDm/En3hcr+VJp+CKkhd3uw/ARDBTb7HdBX7bbJj0m2HWOsQA+RvS8dWw7rNVWF1lhn52skt5btRLWdzsAMwGj6v8bhlbfCIyyVsghhJ9CuSk/67frd5Iaf0Hn7mzOudz7NeUXHWzjnpnhoq2+ZTu5uomwdBfeABOj5xZw5ObhZCq/U45NyDYfth9NLhdSgMdAHwnpIhOlL9vmfoF+gDmhtiXxs9dqX7+vRn5u4Z4Y5yjyjXciqRbAgO82buhevnM8EQk6nUcPtr9+3+5gH26cFdvCO0h1pPPmikLbD/xYHBmH1sd04Hx+bZtTbl+f7QdHRz/d3Ahu460itusJLyYvDvsN2Zr/sn~-1~-1~-1; ak_bmsc=9E468A42656380EC6608B335E017044B~000000000000000000000000000000~YAAQBvttaBy05YKTAQAAyRigmxqF2fJsYdigJ474zq10oLjjIRCzrOPuQc/wRtC06bJFrUn+jCb1rbjJbo0ZutrrYgqcS6PNV6ggBTeWU/b+P+172bTVPa0ol5y537Nr0eDmujSmBQNaYRySPzEwI6/bEHOGfCs+IOxYCVdJd2uK6ZX8J9of03RkcGPRGDgOEJrwwlUxBcXj3bS6sqWsSZ1se4dzz2cDi30ZHhFvTEfoobLCBer2AnLQFnqrBbgtyQzMvuKtNLR5Y0EADh5co4vvQM1eVMTC2od9kEmTNhi7nZbASWp+wRilNxb3zvfKZsFwg3j47/tY4rQNKEnX3fLLm05tHFSkDxgadQ==; bm_sz=A3D7D184406CBB7960FB6C607534DD12~YAAQBvttaB205YKTAQAAyRigmxpVJfED1eTGrHLFdmjvjqEb7e2CWPKYKFLhoejg4aDuoPKFoE3HdnLYLcixvkuZf8Gr8SfRzhYNjtTK1UsdSpXlz6FFulhtiylalr/nXZpZVWkfT5tHf9AUVwaz8WARvj6wRLMjojZlfmoC974tMEO63VwUzLXzKgS6yL1T9PM+EpfoCh364hs+aw+bX0ruOFCnDeiMGvyFfuIGqSituFPMO3s7b1R9DBNkIpwkoTFGlWIzKqxnO3/HDGFSJwPjUKhHn3B4gDHLY54xnxETZ4oumZK1jArwdP0jHx+/+0thaQwb5tVBScOGC2tsAyWru8MjJB0d1cA6R4w5Gw==~4539444~4273977'
    }

    response = requests.request("POST", url, headers=headers, data=payload, timeout=15)
    if response.status_code == 200:
        data = response.json()
        raw_articles = data.get('posts', [])
        extracted_articles = []
        for article in raw_articles:
            title = article.get('title', '')
            link = article.get('url', '')
            full_link = f"https://www.mckinsey.com{link}"
            date = article.get('displayDate', '')
            try:
                formatted_date = datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
            except ValueError:
                formatted_date = date
            
            try:
                content_response = requests.request("GET", full_link, headers=headers, timeout=15)
                content = ""
                if content_response.status_code == 200:
                    soup = BeautifulSoup(content_response.text, 'html.parser')
                    main_content = soup.find('main', class_='mdc-u-grid mdc-u-grid-gutter-xxl')
                    if main_content:
                        content = main_content.get_text(strip=True)
                if not content:
                    continue
                region, keywords = filter_articles_by_region_2(
                    title, content, COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS
                )
                if keywords:
                    extracted_articles_info = ({
                        'title': title,
                        'link': full_link,
                        'content': content,
                        'date': formatted_date,
                        'region': region,
                        'keywords': keywords,
                        'sector': 'banks',
                        'source': 'McKinsey'
                    })
                    save_article(extracted_articles_info)
                    extracted_articles.append(extracted_articles_info)
            except Exception as e:
                print(f"DEBUG: Error fetching article {full_link}: {e}")
                continue

        return extracted_articles
    
def mck_ps_articles():
    url = "https://prd-api.mckinsey.com/api/insightsgrid/articles"

    payload = json.dumps({
      "limit": 11,
      "afterId": "",
      "taxonomyAndTags": {
        "taxonomyQueryType": "OR",
        "taxonomyIds": [
          "c86f5dae-e73d-415c-a94a-36662c9a5237",
          "46898d3c-ba9b-4b62-9a55-c3a61e01d2de",
          "5728cc8a-61c3-4e84-b855-62272de5ef10"
        ],
        "mustHaveTagsQueryType": "OR",
        "mustHaveTags": [
          "0abbc29e-46ee-470b-a93b-c31f735e753a",
          "91cfe105-8dad-437c-8734-3d740dcdb437",
          "15750f40-c2b7-4634-be10-763112fad183",
          "887e7cb2-191e-44d5-9ec6-de040b312a25",
          "a9103a6d-6663-4a30-bf78-9927d74f5df5",
          "21dc6bd4-9b9a-4de0-a9b8-71f68efef898",
          "1ea27058-9b4d-4a64-81f4-f56cb6b81896",
          "aaf8b700-2f9c-40e9-8037-7a90ebf4e651",
          "fcb448f9-af05-4682-a070-ffab859ebdb5",
          "c3f331dd-6683-4c33-9460-e56bb1487f33",
          "899ef466-0f6e-4feb-965d-3882b88ac9a4",
          "13f7e352-920f-4dd2-9a31-f2c3314eb405",
          "fa4bb8d5-ea76-4dd9-9530-2c865a87d5e0",
          "5b69151c-e124-4dcf-b9e7-212b7320050d",
          "83cf99bc-d256-4e4c-a1bf-d0698ec601e9"
        ],
        "mustNotHaveTagsQueryType": "OR",
        "mustNotHaveTags": [
          "a65a9603-c09a-489f-9d77-4afd71c629b3"
        ]
      },
      "excludeItems": [
        "0a7eca10-a81c-43b4-bd18-19ed3620a65a",
        "7a8c73aa-f203-474b-87e3-42464e940faf",
        "0424331e-58a6-4a12-a2dc-5a561a30f3b3",
        "a63ac474-000f-4b47-b608-9846737ab41b",
        "81b6404c-e455-4ca0-b706-ce26aba76357",
        "946a141e-da18-4784-84c1-cfcf3c0e9e20",
        "bd92e8af-6f4e-49bc-8076-43b50fea709d",
        "7366ef39-32f9-4b05-8fe0-1fbde4e377d0",
        "5070b6a0-b5a4-4ddd-892c-735b6eed1154",
        "38c0e2a1-d11d-4912-9b85-8eab38278f6d",
        "041f04e5-a6c1-4eea-8760-46ecd1f85f4c",
        "49f776a5-8f88-403e-a572-7ed3ddfb5c6e",
        "14271181-9120-4ef9-9a29-a48c31a839c5",
        "0a4a5118-3bd0-4dac-a23c-d3e2e07e087d",
        "3012efc1-51e2-4e4e-b571-054b58c20152",
        "09000c94-f55e-41ca-8d2d-0eff5f4f6482",
        "fcc8f9f6-d8fb-4c2e-a5bd-d5f2927f1375",
        "b6315094-71c3-4e27-a87a-2d28c7f4aa81",
        "d593bc9b-b503-48b3-99bc-d6b03d5f0c4b",
        "fa811fd5-250f-4856-9fab-678667324df9",
        "2d762ef2-d53b-4394-84b2-0ece3819d22a",
        "604bc56a-f48f-499c-9230-89ebd807998d",
        "f6badc2c-33ea-4a16-970e-c9bcea9b198c",
        "96a3299c-c0c0-4658-9117-cf72fdd52eed",
        "bf761c76-ee3a-4782-b8c0-51c1fe88a12e",
        "8aac1641-2e28-424c-98d3-3042dad14059",
        "abd2042c-9533-473b-afa6-3f83cc067c36",
        "da3559bd-6657-49ab-87cc-1b57384b457f",
        "fd3fa8bf-35e1-4c96-b197-7112e1e4684d",
        "7a4a10a6-d143-4179-9125-fd0d945de5f4",
        "a9906b80-37ac-431a-9c71-678b502082de"
      ],
      "language": "en",
      "isAlumni": False,
      "filters": []
    })
    headers = {
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/json',
      'origin': 'https://www.mckinsey.com',
      'priority': 'u=1, i',
      'referer': 'https://www.mckinsey.com/industries/public-sector/our-insights',
      'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      'Cookie': '_abck=C682FF2F422B58BFEDF4BAE3E5D039DD~-1~YAAQrKpkXx6VgamTAQAA6LY/qg3AqJv+vYY1atMXSkVxjQKHLroh7LydqszRaBPOZCl5z8iCbGIt+Bu2wtyUyjYRemK6pEj5bT2Dc3NYAAlnOt57fjDME/T+hWQu3nDLGokwYtJtXL1F2Y+d1F86Ilj6zz0/X+baIARiP0Q/3+I4+Ldl7UODM2/lq6r/j8Drs1ePTHUavr6NNpqbGy/KZjCv9t3UXCUqL/9prelKfUCZCwEGMu+mGCqhP7szpuSXmlnKu5c2YyF84XGLYi2CzOKg1wWl7KzrkpC6ewqmwq8Avxu52okbDKfCguc1iiw05FOMgxIFUJ+2IOkXsORvNGc6armp2EBxT4veaMVw7r9YGtTJqUQg/NZvlbtgkY1BklCFcWDa7A4yDc/WIQPt7fsLCABFRi6GTg9zbCqgFb9tz25ZGZ+6PAT2zWtoIdeOskYNE+0lLjajwDv4XwbTEBeFKO04/mSahlKzS6S5MjTmINA=~-1~-1~-1; ak_bmsc=F23CE36FC6D268B3C61191B72409B7A9~000000000000000000000000000000~YAAQrKpkXx+VgamTAQAA6LY/qhpay2jVKuTVDbGTlgEXSZRQNIPeNzS7v8nIZy3jgPv3slnegTjJr/sr8jUuYWEhZzvdID+jsZnZF3RFdQ6wjcYGWaFu8ynY78BveoEiRTfk98E+BhptqSUYqpnx44OqgwmO2xtmJXGAme2x/5ePG0IbEjY6CW7IcafHHMVKhTFA7Uj48geZ3La0R/40Sf/enansnI2krz6Xsck0P5RT06+3tPRyzZJFVvn54IixQELST0ih6pdQYNpQP9F8CmsSSaXZA9QsWxlxWYLbBmsvJ4pC7GzepkPGJM+sqzYkVZ6clLOmDemZCJ6YSaNQuabkc1F7v3ZNhwy48A==; bm_sz=5F0CC42229AFEAB3521CAB2FED416B60~YAAQrKpkXyCVgamTAQAA6LY/qhqpn9mYcyVTz95EkTwF2LLeIvQ4og0Whl3aUi72TeQ88kRMgrqhhDzM9SkhAwyG1wviTgz3wRkquBPPMWREffAean12BACfKfyLa8hglIUXu7NToGnRgMEIDFF7otvTs5TQuYN7ZXC6h9TmpgdrAO4JlmR9RafXp5PMlIYU5Vqmw7SJJHl7Qh13WDafgqju029Df4YqCyL5centMVsYDxR7H4fSyG9Ev7qWa/UT3JWVPQ1rBV7zDGHEFgB0+IGEfPSlyZyXXWnaKSG0IIepUol2Ak79ntlmsvpgvxc9Sz87rGCjOpIVsFXmKsXPLg1G451u7QKJK2yOYi/Sgg==~3158834~4602161'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        raw_articles = data.get('posts', [])
        extracted_articles = []
        for article in raw_articles:
            title = article.get('title', '')
            link = article.get('url', '')
            full_link = f"https://www.mckinsey.com{link}"
            date = article.get('displayDate', '')
            try:
                formatted_date = datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
            except ValueError:
                formatted_date = date

            try:
                response = requests.request("GET", full_link, headers=headers, timeout=10)
                if response.status_code == 200:
                    content = ""
                    soup = BeautifulSoup(response.text, 'html.parser')
                    main_content = soup.find('main', class_='mdc-u-grid mdc-u-grid-gutter-xxl')
                    if main_content:
                        content = main_content.get_text(strip=True)
                    
                    if title and content:
                        region, keywords = filter_articles_by_region_2(title, content, COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS)
                        if keywords:
                            extracted_articles_info = ({
                                'title': title,
                                'link': full_link,
                                'content': content,
                                'date': formatted_date,
                                'region': region,
                                'keywords': keywords,
                                'sector': 'banks',
                                'source': 'McKinsey'
                            })
                            save_article(extracted_articles_info)
                            extracted_articles.append(extracted_articles_info)
                else:
                    print(f"DEBUG: Failed to fetch article {full_link} - Status: {response.status_code}")
            except Exception as e:
                print(f"DEBUG: Error fetching article {full_link}: {e}")
                continue
        return extracted_articles

def mck_fa_articles():
    url = "https://prd-api.mckinsey.com/api/insightsgrid/articles"

    payload = json.dumps({
      "limit": 10,
      "afterId": "",
      "taxonomyAndTags": {
        "taxonomyQueryType": "OR",
        "taxonomyIds": [
          "91cfe105-8dad-437c-8734-3d740dcdb437",
          "0abbc29e-46ee-470b-a93b-c31f735e753a",
          "15750f40-c2b7-4634-be10-763112fad183",
          "21dc6bd4-9b9a-4de0-a9b8-71f68efef898",
          "874ee345-9fa7-403b-bcf3-2eaf719a89fa",
          "1ea27058-9b4d-4a64-81f4-f56cb6b81896",
          "aaf8b700-2f9c-40e9-8037-7a90ebf4e651",
          "fcb448f9-af05-4682-a070-ffab859ebdb5",
          "c3f331dd-6683-4c33-9460-e56bb1487f33",
          "899ef466-0f6e-4feb-965d-3882b88ac9a4",
          "13f7e352-920f-4dd2-9a31-f2c3314eb405",
          "fa4bb8d5-ea76-4dd9-9530-2c865a87d5e0",
          "5b69151c-e124-4dcf-b9e7-212b7320050d",
          "83cf99bc-d256-4e4c-a1bf-d0698ec601e9",
          "a9103a6d-6663-4a30-bf78-9927d74f5df5"
        ],
        "mustHaveTagsQueryType": "OR",
        "mustHaveTags": [
          "8b55ff3d-e6b3-4cc9-8fcd-b817f242672f"
        ],
        "mustNotHaveTagsQueryType": "OR",
        "mustNotHaveTags": [
          "a65a9603-c09a-489f-9d77-4afd71c629b3"
        ]
      },
      "excludeItems": [
        "4a78de41-0ee0-43be-bda4-d644a90b57dc",
        "cd50dd50-ea64-4b47-b9c3-a21a80331630",
        "7b3d4c0a-99f3-4755-be50-322acecea949",
        "733892de-d5ea-477e-994e-1c3c50772e80",
        "15284026-c315-4ccc-9af8-b561b17bcc21",
        "932865d5-c29c-45b5-a1b7-4828f088f7c2",
        "52d53345-1331-41d7-b77b-d55e838766dc",
        "6cf40d71-04fc-43c3-8a6b-9a26be027e92",
        "ed23aa98-ec33-4119-823a-9bb681a4e445",
        "9f899429-fb69-4519-aef5-7311c4c95e72",
        "5bf2b21d-1a36-495f-ad5c-a5a58676b179",
        "ed5317b6-4fb4-4dd7-b0f4-618366e43fdd",
        "{E20A8776-1579-4BBF-9F70-FB67984C75D7}"
      ],
      "language": "en",
      "isAlumni": False,
      "filters": []
    })
    headers = {
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/json',
      'origin': 'https://www.mckinsey.com',
      'priority': 'u=1, i',
      'referer': 'https://www.mckinsey.com/industries/public-sector/our-insights',
      'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
      'Cookie': '_abck=C682FF2F422B58BFEDF4BAE3E5D039DD~-1~YAAQrKpkXx6VgamTAQAA6LY/qg3AqJv+vYY1atMXSkVxjQKHLroh7LydqszRaBPOZCl5z8iCbGIt+Bu2wtyUyjYRemK6pEj5bT2Dc3NYAAlnOt57fjDME/T+hWQu3nDLGokwYtJtXL1F2Y+d1F86Ilj6zz0/X+baIARiP0Q/3+I4+Ldl7UODM2/lq6r/j8Drs1ePTHUavr6NNpqbGy/KZjCv9t3UXCUqL/9prelKfUCZCwEGMu+mGCqhP7szpuSXmlnKu5c2YyF84XGLYi2CzOKg1wWl7KzrkpC6ewqmwq8Avxu52okbDKfCguc1iiw05FOMgxIFUJ+2IOkXsORvNGc6armp2EBxT4veaMVw7r9YGtTJqUQg/NZvlbtgkY1BklCFcWDa7A4yDc/WIQPt7fsLCABFRi6GTg9zbCqgFb9tz25ZGZ+6PAT2zWtoIdeOskYNE+0lLjajwDv4XwbTEBeFKO04/mSahlKzS6S5MjTmINA=~-1~-1~-1; ak_bmsc=F23CE36FC6D268B3C61191B72409B7A9~000000000000000000000000000000~YAAQrKpkXx+VgamTAQAA6LY/qhpay2jVKuTVDbGTlgEXSZRQNIPeNzS7v8nIZy3jgPv3slnegTjJr/sr8jUuYWEhZzvdID+jsZnZF3RFdQ6wjcYGWaFu8ynY78BveoEiRTfk98E+BhptqSUYqpnx44OqgwmO2xtmJXGAme2x/5ePG0IbEjY6CW7IcafHHMVKhTFA7Uj48geZ3La0R/40Sf/enansnI2krz6Xsck0P5RT06+3tPRyzZJFVvn54IixQELST0ih6pdQYNpQP9F8CmsSSaXZA9QsWxlxWYLbBmsvJ4pC7GzepkPGJM+sqzYkVZ6clLOmDemZCJ6YSaNQuabkc1F7v3ZNhwy48A==; bm_sz=5F0CC42229AFEAB3521CAB2FED416B60~YAAQrKpkXyCVgamTAQAA6LY/qhqpn9mYcyVTz95EkTwF2LLeIvQ4og0Whl3aUi72TeQ88kRMgrqhhDzM9SkhAwyG1wviTgz3wRkquBPPMWREffAean12BACfKfyLa8hglIUXu7NToGnRgMEIDFF7otvTs5TQuYN7ZXC6h9TmpgdrAO4JlmR9RafXp5PMlIYU5Vqmw7SJJHl7Qh13WDafgqju029Df4YqCyL5centMVsYDxR7H4fSyG9Ev7qWa/UT3JWVPQ1rBV7zDGHEFgB0+IGEfPSlyZyXXWnaKSG0IIepUol2Ak79ntlmsvpgvxc9Sz87rGCjOpIVsFXmKsXPLg1G451u7QKJK2yOYi/Sgg==~3158834~4602161'
    }

    response = requests.request("POST", url, headers=headers, data=payload, timeout=15)
    if response.status_code == 200:
        data = response.json()
        raw_articles = data.get('posts', [])
        extracted_articles = []
        for article in raw_articles:
            title = article.get('title', '')
            link = article.get('url', '')
            full_link = f"https://www.mckinsey.com{link}"
            date = article.get('displayDate', '')
            try:
                formatted_date = datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
            except ValueError:
                formatted_date = date

            try:
                response = requests.request("GET", full_link, headers=headers, timeout=15)
                if response.status_code == 200:
                    content = ""
                    soup = BeautifulSoup(response.text, 'html.parser')
                    main_content = soup.find('main', class_='mdc-u-grid mdc-u-grid-gutter-xxl')
                    if main_content:
                        content = main_content.get_text(strip=True)

                    if title and content:
                        region, keywords = filter_articles_by_region_2(title, content, COMMON_KEYWORDS, REGIONAL_KEYWORDS, RARE_KEYWORDS)
                        if keywords:
                            extracted_articles_info = ({
                                'title': title,
                                'link': full_link,
                                'content': content,
                                'date': formatted_date,
                                'region': region,
                                'keywords': keywords,
                                'sector': 'banks',
                                'source': 'McKinsey'
                            })
                            save_article(extracted_articles_info)
                            extracted_articles.append(extracted_articles_info)
                else:
                    print(f"DEBUG: Failed to fetch article {full_link} - Status: {response.status_code}")
            except Exception as e:
                print(f"DEBUG: Error fetching article {full_link}: {e}")
                continue
        return extracted_articles

def mck_articles():
    articles = mck() + mck_ps_articles() + mck_fa_articles()
    return articles



