# Pythonning rasmiy tasviridan foydalanish
FROM python:3.8-slim

# Ishchi papkani yaratish va unga o'tish
WORKDIR /app

# Talablar faylini nusxalash
COPY requirements.txt .

# Talablarni o'rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Flask ilovasini nusxalash (agar ilova fayllari mavjud bo'lsa)
COPY . .

# Flaskni ishga tushirish
CMD ["python", "app.py"]
