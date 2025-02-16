# Pythonni o'rnatish
FROM python:3.8-slim

# Ish joyini o'rnatish
WORKDIR /mitmproxy

# `mitmproxy`ni o'rnatish
RUN pip install mitmproxy

# `mitmproxy` skriptini nusxalash
COPY google/search3.py .


# `mitmproxy`ni ishga tushirish
CMD ["mitmdump", "-s", "search3.py"]
