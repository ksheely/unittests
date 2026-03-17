from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"}), 200

@app.route("/add", methods=["POST"])
def add_numbers():
    data = request.get_json()

    if not data or "a" not in data or "b" not in data:
        return jsonify({"error": "Missing a or b"}), 400

    result = data["a"] + data["b"]
    return jsonify({"result": result}), 200