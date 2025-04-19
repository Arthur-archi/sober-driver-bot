import flask
import requests
from flask import request

# === Константы ===
BOT_TOKEN = "8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA"
BOT_URL = "https://api.telegram.org/bot8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA"
ADMIN_CHAT_ID = "7465925576"

app = flask.Flask(__name__)

# Пользовательские языки
user_languages = {}

# Сообщения
MESSAGES = {
    "ru": {
        "start": "👋 Добро пожаловать в сервис «Трезвый водитель Дубай»!\n\n📍 Мы доставим вас и ваш автомобиль в любую точку Дубая.\n📲 Нажмите кнопку ниже, чтобы поделиться геолокацией или связаться с нами.\n\n❓ Вопросы? Напишите @Arthur_01",
        "language": "Выберите язык / Choose your language:",
        "help": "ℹ️ Используйте /order или отправьте геолокацию.",
        "order": "🚘 Отправьте локацию или нажмите WhatsApp.",
        "info": "ℹ️ Работаем 24/7 по Дубаю.",
        "contact": "📞 WhatsApp: +971582615619\n👤 @Arthur_01"
    },
    "en": {
        "start": "👋 Welcome to 'Sober Driver Dubai'!\n\n📍 We will drive you and your car anywhere in Dubai.\n📲 Press the button below to share your location or contact us.\n\n❓ Questions? Message @Arthur_01",
        "language": "Choose your language / Выберите язык:",
        "help": "ℹ️ Use /order or send your location.",
        "order": "🚘 Send location or contact us via WhatsApp.",
        "info": "ℹ️ Available 24/7 in Dubai.",
        "contact": "📞 WhatsApp: +971582615619\n👤 @Arthur_01"
    }
}

def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{BOT_URL}/sendMessage", json=payload)

def get_lang(user_id):
    return user_languages.get(user_id, "ru")

@app.route('/8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA', methods=["POST"])
def webhook():
    update = request.get_json()

    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        user_id = msg["from"]["id"]
        text = msg.get("text", "")

        if text == "/start":
            kb = {
                "keyboard": [[{"text": "🇷🇺 Русский"}, {"text": "🇬🇧 English"}]],
                "resize_keyboard": True
            }
            send_message(chat_id, MESSAGES["ru"]["language"], reply_markup=kb)
            return "ok"

        if text in ["🇷🇺 Русский", "🇷🇺"]:
            user_languages[user_id] = "ru"
            send_message(chat_id, MESSAGES["ru"]["start"])
            return "ok"
        if text in ["🇬🇧 English", "🇬🇧"]:
            user_languages[user_id] = "en"
            send_message(chat_id, MESSAGES["en"]["start"])
            return "ok"

        lang = get_lang(user_id)

        if text in ["/help", "/order", "/info", "/contact"]:
            cmd = text.replace("/", "")
            send_message(chat_id, MESSAGES[lang].get(cmd, ""))
            return "ok"

        if "location" in msg:
            loc = msg["location"]
            maps_link = f"https://maps.google.com/?q={loc['latitude']},{loc['longitude']}"
            send_message(chat_id, "✅ Локация получена! Водитель уже едет." if lang == "ru" else "✅ Location received! Driver is on the way.")
            send_message(ADMIN_CHAT_ID, f"📍 Новый заказ от @{msg['from'].get('username','')}\n🌍 {maps_link}")
            return "ok"

        # Любое другое сообщение
        send_message(chat_id, MESSAGES[lang]["help"])
        return "ok"

    return "ok"

@app.route("/")
def index():
    return "🟢 Бот работает!"
