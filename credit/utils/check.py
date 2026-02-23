import re

def me_related(title, summary, keywords):
    if isinstance(summary, list):
        summary = " ".join(summary)
    elif not isinstance(summary, str):
        summary = ""
    content = title.lower() + " " + summary.lower()
    keyword_mapping = {keyword.lower(): keyword for keyword in keywords}
    pattern = r'\b(?:' + '|'.join(re.escape(keyword.lower()) for keyword in keywords) + r')\b'
    matched_keywords_lower = re.findall(pattern, content)
    matched_keywords_original = sorted({keyword_mapping[kw] for kw in matched_keywords_lower})

    return matched_keywords_original

def is_ca_related(title, summary, keywords):
    if isinstance(summary, list):
        summary = " ".join(summary)
    elif not isinstance(summary, str):
        summary = ""
    content = title.lower() + " " + summary.lower()
    keyword_mapping = {keyword.lower(): keyword for keyword in keywords}
    pattern = r'\b(?:' + '|'.join(re.escape(keyword.lower()) for keyword in keywords) + r')\b'
    matched_keywords_lower = re.findall(pattern, content)
    matched_keywords_original = sorted({keyword_mapping[kw] for kw in matched_keywords_lower})

    return matched_keywords_original

def filter_articles_by_region_2(title, summary, common_keywords, regional_keywords, rare_keywords):
    if isinstance(summary, list):
        summary = " ".join(summary)
    elif not isinstance(summary, str):
        summary = ""
    content = (title + " " + summary).lower()

    matched_regions = set()
    matched_keywords = []

    for region, keywords in rare_keywords.items():
        pattern = r'\b(?:' + '|'.join(re.escape(keyword.lower()) for keyword in keywords) + r')\b'
        rare_matches = re.findall(pattern, content)
        if rare_matches:
            matched_regions.add(region)
            matched_keywords.extend(rare_matches)

    if matched_regions:
        for region, country_keywords in regional_keywords.items():
            country_pattern = r'\b(?:' + '|'.join(re.escape(keyword.lower()) for keyword in country_keywords) + r')\b'
            matched_keywords.extend(re.findall(country_pattern, content))
        common_pattern = r'\b(?:' + '|'.join(re.escape(keyword.lower()) for keyword in common_keywords) + r')\b'
        matched_keywords.extend(re.findall(common_pattern, content))
        matched_keywords = sorted(set(matched_keywords))
        matched_regions = sorted(matched_regions)
        return matched_regions, matched_keywords
    for region, country_keywords in regional_keywords.items():
        country_pattern = r'\b(?:' + '|'.join(re.escape(keyword.lower()) for keyword in country_keywords) + r')\b'
        country_matches = re.findall(country_pattern, content)
        if country_matches:
            common_pattern = r'\b(?:' + '|'.join(re.escape(keyword.lower()) for keyword in common_keywords) + r')\b'
            common_matches = re.findall(common_pattern, content)
            if common_matches:
                matched_regions.add(region)
                matched_keywords.extend(country_matches + common_matches)
    if matched_regions and matched_keywords:
        matched_keywords = sorted(set(matched_keywords))
        matched_regions = sorted(matched_regions)
        return matched_regions, matched_keywords
    return None, None