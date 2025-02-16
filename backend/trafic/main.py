import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash  # Parolni xesh qilish uchun import
import pydivert
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from threading import Thread

# Flask ilovasini yaratish
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True

# Flask-Login konfiguratsiyasi
login_manager = LoginManager()
login_manager.init_app(app)

# Foydalanuvchi sinfini yaratish
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

# Foydalanuvchini yuklash
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(r'D:\apt\python\dis\login.db')  # To'liq yo'l
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE id=?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])  # (id, username, password_hash)
    return None

# Fayldan kalit so'zlarni o'qish
def load_keywords_from_txt(filename):
    keywords = []
    try:
        with open(filename, 'r') as file:
            keywords = [line.strip() for line in file.readlines() if line.strip()]
    except Exception as e:
        print(f"[-] Error reading the TXT file: {e}")
    return keywords

# Tarmoq paketlarini bloklash
def block_packets():
    print("[*] Starting packet interception...")

    # Fayldan kalit so'zlarni o'qish
    blocked_keywords = load_keywords_from_txt('blocked_keywords.txt')  # blocked_keywords.txt fayli

    if not blocked_keywords:
        print("[-] No blocked keywords found. Exiting...")
        return
    
    # Barcha TCP paketlarini bloklash
    with pydivert.WinDivert("tcp.PayloadLength > 0") as w:
        for packet in w:
            try:
                # Paket ichidagi ma'lumotlarni tekshirish
                if packet.payload:
                    payload_data = packet.payload.decode(errors="ignore")

                    # Paketda fayl ma'lumotlari bo'lsa, faylni tekshirish
                    if any(payload_data.endswith(ext) for ext in ['.txt', '.docx']):
                        print(f"[*] Checking file content in packet: {payload_data[:100]}...")

                        # Fayl tarkibida kalit so'zlarni tekshirish
                        for keyword in blocked_keywords:
                            if keyword in payload_data:
                                print(f"[!] Blocked packet containing: {keyword}")
                                break
                        else:
                            # Agar kalit so'z topilmasa, paketni o'tkazish
                            w.send(packet)
                    else:
                        # Fayl emas, boshqa paketlarni o'tkazish
                        w.send(packet)
                else:
                    # Paketni o'tkazish
                    w.send(packet)
            except Exception as e:
                print(f"[-] Error processing packet: {e}")

# Web interface uchun route
@app.route('/')
def index():
    if current_user.is_authenticated:
        keywords = load_keywords_from_txt('blocked_keywords.txt')
        return render_template('index.html', keywords=keywords)
    return redirect(url_for('login'))

# Kalit so'z qo'shish
@app.route('/add_keyword', methods=['POST'])
@login_required
def add_keyword():
    keyword = request.form.get('keyword')
    if keyword:
        with open('blocked_keywords.txt', 'a') as file:
            file.write(keyword + '\n')
    return redirect(url_for('index'))

# Kalit so'z o'chirish
@app.route('/delete_keyword/<string:keyword>')
@login_required
def delete_keyword(keyword):
    keywords = load_keywords_from_txt('blocked_keywords.txt')
    keywords.remove(keyword)

    # Yangilangan kalit so'zlarni faylga yozish
    with open('blocked_keywords.txt', 'w') as file:
        file.writelines([k + '\n' for k in keywords])
    
    return redirect(url_for('index'))

# Login sahifasi
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = sqlite3.connect(r'D:\apt\python\dis\login.db')

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username=?", (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data and check_password_hash(user_data[2], password):
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)
            return redirect(url_for('index'))
        else:
            return "Login yoki parol xato", 401

    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Dastur ishga tushirish
def run_flask():
    app.run(host='0.0.0.0', port=5000, use_reloader=False)  # signal muammosini bartaraf etish uchun use_reloader=False

def run_packet_blocking():
    block_packets()

if __name__ == '__main__':
    # Flask ilovasini alohida oqimda ishga tushirish
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Tarmoq paketlarini bloklashni alohida oqimda ishga tushirish
    packet_thread = Thread(target=run_packet_blocking)
    packet_thread.start()

    # Oqimlarni kutish
    flask_thread.join()
    packet_thread.join()
