from flask import Flask, request

app = Flask(__name__)

@app.route('/filter', methods=['POST'])
def filter_request():
    data = request.json
    if data["user_role"] >= data["file_role"]:
        return {"status": "allowed"}
    return {"status": "blocked"}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
