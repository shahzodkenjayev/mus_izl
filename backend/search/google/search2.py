import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

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

# Oddiy HTTP server
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        terms = load_terms("blocked_terms.txt")
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Qidiruv parametrini olish (masalan, "q")
        search_query = query_params.get("q", [""])[0]
        
        if contains_blocked_terms(search_query, terms):
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Blocked: Your search contains restricted terms.")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Search allowed.")

# Serverni ishga tushirish
def run_server(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
