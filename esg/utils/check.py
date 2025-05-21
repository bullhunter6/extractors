from utils.keywords import ESG_KEYWORDS

def is_esg_related(title, summary):
    if isinstance(summary, list):
        summary = " ".join(summary)
    elif not isinstance(summary, str):
        summary = ""
    content = title.lower() + " " + summary.lower()
    matched_keywords = [keyword for keyword in ESG_KEYWORDS if keyword.lower() in content]
    return matched_keywords
