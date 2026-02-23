import requests
from utils.db import save_publication

def weforum_publications():
    url = "https://www.weforum.org/graphql?operationName=ReportsFilteredSearch&variables=%7B%22centres%22%3A%22%22%2C%22years%22%3A%22%22%2C%22topics%22%3A%22%22%2C%22types%22%3A%22%22%2C%22page%22%3A1%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2243dca782c991ef308403990020ba288c0ca7d95f2502347df5d2c073f7f9ffd2%22%7D%7D"

    headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': '_vwo_uuid_v2=D9337D972C5B9BC0007310E700C442F0F|0252ed669c2d61532b8730f2ac4ac363; _vis_opt_s=1%7C; _vis_opt_test_cookie=1; _vwo_uuid=D9337D972C5B9BC0007310E700C442F0F; _vwo_sn=0%3A1; _vwo_ds=3%3At_0%2Ca_0%3A0%241734347474%3A47.76191606%3A%3A109_0%2C26_0%3A4_0%2C3_0%3A0; CookieConsent={stamp:%270Pe0pt2rYeUUpP3j04jw1NJ6i7zz09WfBN3p/dQzM/5bvz27JpiEJg==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1734347483048%2Cregion:%27ae%27}; _gcl_au=1.1.772470363.1734347482; _ga=GA1.1.1388714862.1734347475; mpDistinctId=e310ab7a-20ef-4aec-8543-f1571338da5d; mp_6232aeb08818ee1161204a011ed8ad16_mixpanel=%7B%22distinct_id%22%3A%20%22e310ab7a-20ef-4aec-8543-f1571338da5d%22%2C%22%24device_id%22%3A%20%22193cf2a664d2791-0bf295d60a63e4-26011851-1fa400-193cf2a664d2791%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22%24user_id%22%3A%20%22e310ab7a-20ef-4aec-8543-f1571338da5d%22%2C%22platform%22%3A%20%22Public%20Site%22%7D; gtm_session_start=1734347494861; _web_session=RnR1SnEza3R0eHlaaFJ6U2FpS1Q2U3BwcjhueHg3TFIxYVFxdnY4OTRqa3dPSTFCaE41SkUzRWFOU3A3QzNpdWRlVXFObERyeGRicWxoWjdjV1IrQ3JEKzVPam1hME1MWHBGZ3d1dEtWNnVRcngzQk90MUVCNXBNRy9OVmp4N2hERSs1cFFwM2syZEpJZWMzdkZSajN3PT0tLXl5c1gzMjRWcUtZUU9heFg4VzZvenc9PQ%3D%3D--61ffea1865ca250c1b6780790e806a066406cce6; _ga_4DKG1LX6QK=GS1.1.1734347476.1.1.1734347509.33.0.0; _ga_1RV0X04XBG=GS1.1.1734347475.1.1.1734347510.0.0.0; _ga_2K5FR2KRN5=GS1.1.1734347475.1.1.1734347510.32.0.0',
    'If-None-Match': 'W/"ac768721a79ff421f2e852ae0bcdadfd"',
    'Referer': 'https://www.weforum.org/publications/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'X-CSRF-Token': 'c8Z/zfM1iT9SEv+ZWUWj+R6cu03XFpaF99HR1wQOzyTDvtyaEB7l2EdUNwPuGE0AZ8mGqlaS6U69lwLFW50dMw==',
    'accept': '*/*',
    'content-type': 'application/json',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.get(url, headers=headers)
    publications = []
    
    if response.status_code == 200:
        data = response.json()
        for report in data['data']['reportsFilteredSearch']['reports']:
            title = report.get('title', 'No title')
            description = report.get('description', 'No description')
            link = report.get('url', '#')
            date = report.get('publishedAt', 'No date')
            image = report.get('image', {}).get('url', 'No image')
            
            publication = {
                'title': title,
                'description': description,
                'link': link,
                'date': date,
                'image': image
            }
            publications.append(publication)
            save_publication(publication, source="weforum")
    else:
        print(f"Error fetching data: {response.status_code}")

    return publications



