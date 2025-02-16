from flask import Flask, render_template, request, redirect, url_for, session
import os
import subprocess

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Flask session uchun maxfiy kalit

TERMS_FILE = "terms.txt"

# Barcha terminlarni o'qish
def read_terms():
    if not os.path.exists(TERMS_FILE):
        return []
    with open(TERMS_FILE, "r") as file:
        return [line.strip() for line in file.readlines()]

# Yangi terminlarni qo'shish
def add_term(term):
    with open(TERMS_FILE, "a") as file:
        file.write(term + "\n")

# Terminlarni o'chirish
def delete_term(term):
    terms = read_terms()
    terms = [t for t in terms if t != term]
    with open(TERMS_FILE, "w") as file:
        file.write("\n".join(terms) + "\n")

# Administrator uchun login va parol
ADMIN_DATA = {"username": "admin", "password": "admin123"}

@app.route("/")
def home():
    terms = read_terms()
    return render_template("index.html", terms=terms)

@app.route("/add", methods=["POST"])
def add():
    term = request.form.get("term")
    if term:
        add_term(term)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    term = request.form.get("term")
    if term:
        delete_term(term)
    return redirect("/")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_DATA["username"] and password == ADMIN_DATA["password"]:
            session['admin'] = True  # Administrator sifatida tizimga kirish
            return redirect(url_for('admin_dashboard'))
        else:
            return "<h2>Invalid username or password</h2>"

    return render_template("login.html")

@app.route('/admin')
def admin_dashboard():
    # Agar foydalanuvchi admin bo'lsa, faqat shu sahifaga kirishga ruxsat beriladi
    if 'admin' in session:
        terms = read_terms()
        return render_template("admin_dashboard.html", terms=terms)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('admin', None)  # Administratorni chiqish qilish
    return redirect(url_for('home'))

@app.route("/admin/add", methods=["POST"])
def admin_add():
    if 'admin' in session:
        term = request.form.get("term")
        if term:
            add_term(term)
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('login'))

@app.route("/admin/delete", methods=["POST"])
def admin_delete():
    if 'admin' in session:
        term = request.form.get("term")
        if term:
            delete_term(term)
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('login'))

# search_blokirovka tugmasi bosilganda mitmproxyni ishga tushirish
@app.route("/search_blokirovka", methods=["POST"])
@app.route("/search_blokirovka", methods=["POST"])
def search_blokirovka():
    if 'admin' in session:
        # CMD buyruqni bajarish
        command = r"mitmdump -s D:\apt\python\dis1\google\search3.py"  # To'g'ri yo'l formatida
        try:
            # subprocess yordamida CMD buyruqni ishga tushiramiz
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            print(result.stdout)  # Bu yerda konsolga natijani chiqarish
            return redirect(url_for('admin_dashboard'))
        except subprocess.CalledProcessError as e:
            print(f"Xatolik yuz berdi: {e.stderr}")  # Xatolikni konsolga chiqarish
            return f"<h2>Muammo yuz berdi: {e.stderr}</h2>"
    else:
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

