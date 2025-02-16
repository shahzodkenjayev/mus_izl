from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask serveri ishga tushdi!"

if __name__ == "__main__":
    # Flask serverini barcha tarmoq manzillaridan ulanishga ruxsat berish
    app.run(host='0.0.0.0', port=5000, debug=True)
