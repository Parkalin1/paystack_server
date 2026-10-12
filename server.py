from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)
PAYSTACK_SECRET = os.environ.get("PAYSTACK_SECRET")

PRODUCTS = {
    "facebook": 250000,
    "instagram": 250000,
    "telegram": 500000,
    "twitter": 500000,
    "whatsapp": 600000
}

@app.route('/pay', methods=['POST'])
def create_payment():
    data = request.json
    product = data.get('product')
    email = data.get('email')
    amount = PRODUCTS.get(product)
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET}"}
    body = {"email": email, "amount": amount}
    res = requests.post("https://api.paystack.co/transaction/initialize", json=body, headers=headers)
    return jsonify(res.json())

@app.route('/')
def home():
    return "Server Running!"

if __name__ == '__main__':
    app.run()