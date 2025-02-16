import sqlite3
import os
from werkzeug.security import generate_password_hash  # Parolni xesh qilish uchun import

# Fayl nomi
db_file = 'login.db'

# Fayl mavjudligini tekshirib ko'rish
if not os.path.exists(db_file):
    print("Database file does not exist. Creating a new one...")

    # Faylni yaratish
    conn = sqlite3.connect(db_file)  # Faylni yaratadi yoki unga ulanadi
    cursor = conn.cursor()

    # Jadval yaratish
    cursor.execute('''CREATE TABLE IF NOT EXISTS admin (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        username TEXT NOT NULL, 
                        password_hash TEXT NOT NULL)''')  # password_hash nomini ishlatish

    # Ma'lumotlar qo'shish (agar kerak bo'lsa)
    # Parolni xesh qilish
    password_hash = generate_password_hash('admin')  # admin parolini xesh qilish
    cursor.execute("INSERT INTO admin (username, password_hash) VALUES (?, ?)", ('admin', password_hash))

    # O'zgarishlarni saqlash va bog'lanishni yopish
    conn.commit()
    conn.close()

    print("Database file created and initial data inserted.")
else:
    print("Database file already exists.")
