from rau_config import CONSTITUENCY, RAU_LOCATION_TERMS, PARTIES, CANDIDATES_LEADERS, ISSUES

def contains_any(text, terms):
    text_l = str(text).lower()
    return any(str(term).lower() in text_l for term in terms)

def is_rau_related(text):
    return contains_any(text, RAU_LOCATION_TERMS)

def detect_entity(text):
    # Candidate/leader has priority
    for name, aliases in CANDIDATES_LEADERS.items():
        if contains_any(text, aliases):
            return name, "candidate/leader"

    for party, aliases in PARTIES.items():
        if contains_any(text, aliases):
            return party, "party"

    return "General Rau", "general"

def detect_issue(text):
    matched = []
    for issue, aliases in ISSUES.items():
        if contains_any(text, aliases):
            matched.append(issue)

    return ", ".join(matched) if matched else "General"

def build_row(platform, source_name, text, keyword, created_at, sentiment, score, source_url):
    entity, entity_type = detect_entity(text + " " + keyword)
    issue = detect_issue(text + " " + keyword)

    return {
        "state": CONSTITUENCY["state"],
        "constituency_no": CONSTITUENCY["constituency_no"],
        "constituency": CONSTITUENCY["constituency"],
        "district": CONSTITUENCY["district"],
        "region": CONSTITUENCY["region"],
        "platform": platform,
        "source_name": source_name,
        "text": text,
        "keyword": keyword,
        "matched_entity": entity,
        "entity_type": entity_type,
        "issue_category": issue,
        "created_at": created_at,
        "sentiment": sentiment,
        "sentiment_score": score,
        "source_url": source_url
    }
