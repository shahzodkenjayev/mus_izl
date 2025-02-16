from mitmproxy import http
import os
import datetime

# Terminlarni yuklash uchun fayl yo'li
TERMIN_FILE = "termin.txt"

# Amal qilish vaqtini tahlil qilish funksiyasi
def parse_expiry_time(expiry_str):
    now = datetime.datetime.now()
    time_units = {
        "soat": 3600,
        "daqiqa": 60,
        "kun": 86400
    }
    try:
        # Amal qilish vaqtini <raqam> <birlik> formatida tahlil qilish
        amount, unit = expiry_str.split()
        amount = int(amount)
        if unit not in time_units:
            raise ValueError(f"Noma'lum vaqt birligi: {unit}")
        return now + datetime.timedelta(seconds=amount * time_units[unit])
    except Exception as e:
        print(f"Xato: Amal qilish vaqtini tahlil qilib bo‘lmadi: {expiry_str}. {e}")
        return now  # Xato bo‘lsa, darhol amal qilish muddati tugadi deb hisoblanadi

# Bloklanadigan terminlar va ularning amal qilish vaqtlarini yuklash
def load_terms():
    if not os.path.exists(TERMIN_FILE):
        print(f"Fayl topilmadi: {TERMIN_FILE}")
        return []
    
    terms = []
    with open(TERMIN_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                # Fayldagi qatordan termin va vaqtni ajratib o‘qiymiz
                term, expiry_str = line.split(",")
                term = term.strip().lower()
                expiry_date = parse_expiry_time(expiry_str.strip())
                terms.append((term, expiry_date))
            except ValueError:
                print(f"Xatolik: noto'g'ri format: {line}")
    return terms

# Bloklanadigan terminlar ro'yxati (termin, amal qilish vaqti)
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
    now = datetime.datetime.now()

    # Amal qilish muddatini tekshirib, terminlarni filtrlaymiz
    valid_terms = [(term, expiry) for term, expiry in blocked_terms if expiry > now]
    
    for term, expiry in valid_terms:
        if term in url:  # URLda bloklanadigan termin borligini tekshirish
            print(f"Bloklangan URL: {url} (amal qilish muddati: {expiry})")
            block_request(flow)
            return

    # So‘rov ichidagi ma'lumotlarni ham tekshirish (agar POST/GET parametrlarida bo‘lsa)
    if flow.request.text:
        for term, expiry in valid_terms:
            if term in flow.request.text.lower():
                print(f"Bloklangan ma'lumot: {flow.request.text} (amal qilish muddati: {expiry})")
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
