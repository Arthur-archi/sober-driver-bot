from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA"
URL = f"https://api.telegram.org/bot{TOKEN}"

@app.route("/", methods=["GET"])
def index():
    return "Бот работает!"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Получены данные:", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        reply = "Привет! Это Трезвый водитель Дубай 🚗"

        requests.post(f"{URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": reply
        })

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
