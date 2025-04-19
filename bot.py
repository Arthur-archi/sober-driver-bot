from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
WEBHOOK_URL = "https://sober-driver-dubai.up.railway.app"

# === УСТАНОВКА ВЕБХУКА ===
@app.route("/set_webhook")
def set_webhook():
    url = f"{TELEGRAM_API_URL}/setWebhook"
    data = {"url": f"{WEBHOOK_URL}/webhook"}
    response = requests.post(url, json=data)
    return response.json()

# === ОБРАБОТЧИК ВЕБХУКА ===
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        send_message(chat_id, f"Вы написали: {text}")
    
    return {"ok": True}

# === ОТПРАВКА СООБЩЕНИЯ ===
def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

# === СТАРТ СЕРВЕРА ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
