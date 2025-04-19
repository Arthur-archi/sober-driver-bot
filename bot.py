from flask import Flask, request
import requests
import os

app = Flask(__name__)

# === НАСТРОЙКИ ===
TOKEN = "8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}"
WEBHOOK_URL = "https://sober-driver-dubai.up.railway.app/webhook"

# === ГЛАВНАЯ СТРАНИЦА ===
@app.route('/')
def home():
    return 'Бот "Трезвый водитель Дубай" работает!'

# === УСТАНОВКА ВЕБХУКА ===
@app.route('/set_webhook')
def set_webhook():
    webhook_url = f"{TELEGRAM_API_URL}/setWebhook?url={WEBHOOK_URL}"
    response = requests.get(webhook_url)
    return response.json()

# === ОБРАБОТКА ВЕБХУКА ===
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_welcome(chat_id)
        else:
            send_message(chat_id, "Спасибо! Мы получили ваше сообщение.")

    return "ok", 200

# === ФУНКЦИИ ОТПРАВКИ ===
def send_message(chat_id, text, reply_markup=None):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": reply_markup,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

def send_welcome(chat_id):
    text = (
        "🚖 <b>Трезвый водитель Дубай</b>\n\n"
        "Добро пожаловать! Мы оперативно доставим вас и ваше авто домой.\n\n"
        "📍 Отправьте геолокацию\n"
        "📞 Позвоните: +971582615619\n"
        "💬 Или напишите в WhatsApp"
    )

    keyboard = {
        "keyboard": [
            [{"text": "📍 Отправить геолокацию", "request_location": True}],
            [{"text": "📞 Позвонить", "url": "tel:+971582615619"}],
            [{"text": "💬 WhatsApp", "url": "https://wa.me/971582615619"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }

    send_message(chat_id, text, reply_markup=keyboard)

# === ЗАПУСК СЕРВЕРА ===
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
