from mitmproxy import http
import os

# Terminlarni yuklash uchun fayl yo'li
TERMIN_FILE = "termin.txt"

# Bloklanadigan terminlarni yuklaymiz
def load_terms():
    if not os.path.exists(TERMIN_FILE):
        print(f"Fayl topilmadi: {TERMIN_FILE}")
        return []
    with open(TERMIN_FILE, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

# Bloklanadigan terminlar ro'yxati
blocked_terms = load_terms()

# Foydalanuvchini xabar bilan bloklangan sahifaga yo‘naltirish
def block_request(flow: http.HTTPFlow):
    flow.response = http.Response.make(
        403,  # HTTP status code: Forbidden
        b"Bu so'rov bloklandi! Ruxsat berilmagan kontent.",  # Xabar
        {"Content-Type": "text/plain"}  # Javob turi
    )

# HTTP/HTTPS so‘rovlarini tekshirish
def request(flow: http.HTTPFlow):
    global blocked_terms
    url = flow.request.pretty_url.lower()
    for term in blocked_terms:
        if term in url:  # URLda bloklanadigan termin borligini tekshirish
            print(f"Bloklangan URL: {url}")
            block_request(flow)
            return

    # So‘rov ichidagi ma'lumotlarni ham tekshirish (agar POST/GET parametrlarida bo‘lsa)
    if flow.request.text:
        for term in blocked_terms:
            if term in flow.request.text.lower():
                print(f"Bloklangan ma'lumot: {flow.request.text}")
                block_request(flow)
                return

# Terminalda bloklangan URLlarni qayta yuklash
def reload_terms(flow: http.HTTPFlow):
    if "reload_terms" in flow.request.pretty_url:
        global blocked_terms
        blocked_terms = load_terms()
        flow.response = http.Response.make(
            200,  # HTTP status code: OK
            b"Terminlar qayta yuklandi!",
            {"Content-Type": "text/plain"}
        )

# Javobni boshqarish uchun
def response(flow: http.HTTPFlow):
    reload_terms(flow)
