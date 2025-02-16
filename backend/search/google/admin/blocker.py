from flask import Flask, request, jsonify, render_template
from mitmproxy import http
import os
import socket

# Fayllar va sozlamalar
TERMIN_FILE = "termin.txt"
ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "admin123"

# Flask ilovasi yaratish
app = Flask(__name__)

# Bloklanadigan terminlar ro‘yxatini yuklash
def load_terms():
    if not os.path.exists(TERMIN_FILE):
        return []
    with open(TERMIN_FILE, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

# Global termin ro‘yxati
blocked_terms = load_terms()

# Faylga terminlarni yozish
def save_terms():
    with open(TERMIN_FILE, "w", encoding="utf-8") as f:
        f.writelines([term + "\n" for term in blocked_terms])

# Internetni cheklash funksiyasi
def block_internet():
    try:
        # Barcha so‘rovlarni "localhost" bilan cheklash
        socket.create_connection(("localhost", 80), timeout=1)
    except Exception:
        pass  # Internetga ulanish muvaffaqiyatsiz bo‘lsa, hech narsa qilmaydi

# Internetni tiklash funksiyasi
def allow_internet():
    pass  # Agar kerak bo‘lsa, tarmoq sozlamalarini qayta yoqish funksiyasi qo‘shiladi

# Admin veb-interfeys
@app.route('/')
def admin_panel():
    return render_template("admin.html", terms=blocked_terms)

@app.route('/add_term', methods=['POST'])
def add_term():
    global blocked_terms
    new_term = request.form.get('term', '').lower()
    if new_term and new_term not in blocked_terms:
        blocked_terms.append(new_term)
        save_terms()
        return jsonify({"status": "success", "message": f"Termin qo'shildi: {new_term}"})
    return jsonify({"status": "error", "message": "Termin mavjud yoki noto'g'ri."})

@app.route('/remove_term', methods=['POST'])
def remove_term():
    global blocked_terms
    term = request.form.get('term', '').lower()
    if term in blocked_terms:
        blocked_terms.remove(term)
        save_terms()
        return jsonify({"status": "success", "message": f"Termin o'chirildi: {term}"})
    return jsonify({"status": "error", "message": "Termin topilmadi."})

@app.route('/toggle_internet', methods=['POST'])
def toggle_internet():
    action = request.form.get('action', '')
    if action == "block":
        block_internet()
        return jsonify({"status": "success", "message": "Internet cheklangan."})
    elif action == "allow":
        allow_internet()
        return jsonify({"status": "success", "message": "Internetga ruxsat berildi."})
    return jsonify({"status": "error", "message": "Noto‘g‘ri so‘rov."})

# Mitmproxy funksiyasi: HTTP so‘rovlarni boshqarish
def request(flow: http.HTTPFlow):
    global blocked_terms
    url = flow.request.pretty_url.lower()

    # URL ichida bloklangan terminlarni qidirish
    for term in blocked_terms:
        if term in url:
            flow.response = http.Response.make(
                403,  # HTTP status code: Forbidden
                b"Bu so'rov bloklandi! Ruxsat berilmagan kontent.",
                {"Content-Type": "text/plain"}
            )
            return

# Flask ilovasini ishga tushirish
def start_admin_interface():
    app.run(host="0.0.0.0", port=5000, debug=True)

# Flask serverni asosiy jarayonda ishga tushirish
if __name__ == "__main__":
    start_admin_interface()
