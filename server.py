from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

PAYSTACK_SECRET = os.environ.get("PAYSTACK_SECRET_KEY")

@app.route("/initialize", methods=["POST", "OPTIONS"])
def initialize():
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
        return response, 200
    try:
        data = request.get_json()
        email = data.get("email")
        amount = data.get("amount")
        if not email or not amount:
            return jsonify({"status": False, "message": "email and amount required"}), 400
        headers = {"Authorization": f"Bearer {PAYSTACK_SECRET}", "Content-Type": "application/json"}
        payload = {"email": email, "amount": int(amount)}
        resp = requests.post("https://api.paystack.co/transaction/initialize", json=payload, headers=headers)
        result = resp.json()
        return jsonify(result), resp.status_code
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Paystack Server Running - Use POST /initialize"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)