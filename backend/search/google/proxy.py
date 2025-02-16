from mitmproxy import http
import re

# txt fayldan terminlarni o'qish
def load_terms(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip().lower() for line in file if line.strip()]

# Qidiruv so'rovini tekshirish
def contains_blocked_terms(query, terms):
    for term in terms:
        if re.search(r'\b' + re.escape(term) + r'\b', query, re.IGNORECASE):
            return True
    return False

# Proxy so'rovlarni boshqarish
def request(flow: http.HTTPFlow) -> None:
    terms = load_terms("blocked_terms.txt")
    if "google.com/search" in flow.request.pretty_url:
        query = flow.request.query.get("q", "")
        if contains_blocked_terms(query, terms):
            flow.response = http.Response.make(
                403,
                b"Bloklangan: Qidiruvingizda taqiqlangan terminlar mavjud.",
                {"Content-Type": "text/plain"},
            )
