from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = '8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA'
ADMIN_ID = '7465925576'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, json=payload)

@app.route('/', methods=['GET'])
def index():
    return '✅ Webhook работает (GET)', 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # Ответ клиенту
        send_message(chat_id, "Спасибо за сообщение! Мы скоро свяжемся с вами.")

        # Уведомление админу
        send_message(ADMIN_ID, f"📩 Новое сообщение от клиента:\nID: {chat_id}\nТекст: {text}")

    return '✅ OK', 200

# 🚫 Не нужно запускать Flask вручную!
# Railway запускает gunicorn, этот блок удалён
