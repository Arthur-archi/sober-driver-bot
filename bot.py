from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA"
ADMIN_ID = 7465925576

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route('/')
def index():
    return "✅ Бот успешно работает на Railway!"

@app.route('/set_webhook')
def set_webhook():
    webhook_url = "https://sober-driver-dubai.up.railway.app/webhook"
    url = f"{TELEGRAM_API_URL}/setWebhook?url={webhook_url}"
    response = requests.get(url)
    return response.json()

@app.route('/webhook', methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text == "/start":
            send_message(chat_id,
                         "🚘 <b>Трезвый водитель Дубай</b>\n\n"
                         "📍 Мы доставим вас и ваш автомобиль в любую точку Дубая.\n"
                         "📲 Нажмите, чтобы отправить геолокацию или связаться с администратором.\n\n"
                         "❓ В случае вопросов — @Arthur_01",
                         parse_mode="HTML")
        else:
            send_message(chat_id, f"✅ Вы написали: {text}")

    return {"ok": True}

def send_message(chat_id, text, parse_mode=None):
    data = {"chat_id": chat_id, "text": text}
    if parse_mode:
        data["parse_mode"] = parse_mode
    requests.post(f"{TELEGRAM_API_URL}/sendMessage", json=data)
