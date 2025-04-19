import os
import requests
from flask import Flask, request

# 1) Настройки — токен и айди администратора
BOT_TOKEN = "8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA"
ADMIN_ID = "7465925576"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = Flask(__name__)

# Языковые шаблоны
START_TEXT = {
    "ru": (
        "👋 Добро пожаловать в сервис «Трезвый водитель Дубай»!\n\n"
        "📍 Мы доставим вас и ваш автомобиль в любую точку Дубая.\n"
        "📲 Нажмите кнопку ниже, чтобы поделиться геолокацией или связаться с нами.\n\n"
        "❓ Если что-то непонятно — напишите администратору: @Arthur_01"
    ),
    "en": (
        "👋 Welcome to “Sober Driver Dubai” service!\n\n"
        "📍 We will deliver you and your car anywhere in Dubai.\n"
        "📲 Press the button below to share your location or contact us.\n\n"
        "❓ If something is unclear — contact the admin: @Arthur_01"
    )
}
THANKS_TEXT = {
    "ru": (
        "✅ Спасибо! Мы получили вашу геолокацию.\n\n"
        "Пожалуйста, напишите:\n"
        "1️⃣ Адрес назначения (точка Б)\n"
        "2️⃣ Марку и модель автомобиля\n"
        "3️⃣ Номер машины (если есть)\n"
        "4️⃣ Контактный номер для связи\n"
        "5️⃣ Уточнения или пожелания (по времени, срочности и т.д.)"
    ),
    "en": (
        "✅ Thank you! We received your location.\n\n"
        "Please write:\n"
        "1️⃣ Destination address (point B)\n"
        "2️⃣ Car brand and model\n"
        "3️⃣ Car number (if any)\n"
        "4️⃣ Contact number\n"
        "5️⃣ Comments or wishes (urgency, time, etc.)"
    )
}


def detect_lang(code: str) -> str:
    return "en" if code and code.startswith("en") else "ru"


def send_message(chat_id, text, reply_markup=None):
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(f"{API_URL}/sendMessage", json=data)


def build_keyboard(lang: str):
    return {
        "keyboard": [
            [{"text": "📍 Отправить геолокацию", "request_location": True}],
            [{"text": "📞 Позвонить"}],
            [{"text": "💬 WhatsApp"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }


@app.route("/", methods=["GET"])
def index():
    return "🟢 Bot is alive", 200


@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    RAILWAY_URL = "https://worker-production-9f3f.up.railway.app"
    hook = f"{RAILWAY_URL}/{BOT_TOKEN}"
    res = requests.get(f"{API_URL}/setWebhook?url={hook}")
    return res.json(), 200


@app.route(f"/{BOT_TOKEN}", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return "▶️ Webhook endpoint", 200

    data = request.get_json(force=True)
    if "message" in data:
        msg = data["message"]
        chat_id = msg["chat"]["id"]
        user_lang = detect_lang(msg["from"].get("language_code", ""))

        # Команда /start
        if msg.get("text", "").startswith("/start"):
            send_message(chat_id, START_TEXT[user_lang], reply_markup=build_keyboard(user_lang))
            return {"ok": True}

        # Геолокация
        if "location" in msg:
            link = f"https://www.google.com/maps?q={msg['location']['latitude']},{msg['location']['longitude']}"
            send_message(chat_id, THANKS_TEXT[user_lang])
            admin_msg = (
                f"📬 Новый заказ от @{msg['from'].get('username','—')}:\n"
                f"📍 Геолокация: {link}"
            )
            send_message(ADMIN_ID, admin_msg)
        else:
            # Другое сообщение — пересылаем админу
            user = msg["from"]
            forward = f"📩 Ответ от {user.get('first_name','')}:\n{msg.get('text','')}"
            send_message(ADMIN_ID, forward)
    return {"ok": True}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
