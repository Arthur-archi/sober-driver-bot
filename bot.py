import os
from flask import Flask, request
import requests
import json

TOKEN = '8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA'
BOT_URL = f'https://api.telegram.org/bot{TOKEN}'
ADMIN_CHAT_ID = '7465925576'

app = Flask(__name__)

messages = {
    "ru": {
        "welcome": "👋 Добро пожаловать в сервис «Трезвый водитель Дубай»!\n\n📍 Мы доставим вас и ваш автомобиль в любую точку Дубая.\n\n🧭 Нажмите кнопку ниже, чтобы поделиться геолокацией или связаться с нами.\n\n❓ Если что-то непонятно — напишите администратору:\n@Arthur_01",
        "choose_lang": "Выберите язык / Choose your language:"
    },
    "en": {
        "welcome": "👋 Welcome to the 'Sober Driver Dubai' service!\n\n📍 We will drive you and your car anywhere in Dubai.\n\n🧭 Press the button below to share your location or contact us.\n\n❓ If you have any questions — contact admin:\n@Arthur_01",
        "choose_lang": "Choose your language / Выберите язык:"
    }
}

def get_keyboard(lang):
    return {
        "keyboard": [
            [{"text": "📍 Отправить геолокацию / Share Location", "request_location": True}],
            [{"text": "📞 Позвонить / Call", "url": "tel:+971582615619"}],
            [{"text": "💬 WhatsApp", "url": "https://wa.me/971582615619"}],
            [{"text": "🌐 Language / Язык"}]
        ],
        "resize_keyboard": True
    }

def detect_language(user_lang):
    return "ru" if user_lang.startswith("ru") else "en"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()

    if 'message' in data:
        message = data['message']
        chat_id = message['chat']['id']
        user_lang = message['from'].get('language_code', 'en')
        lang = detect_language(user_lang)

        if 'text' in message:
            text = message['text'].lower()

            if text in ['/start', 'start']:
                send_message(chat_id, messages[lang]['welcome'], get_keyboard(lang))

                requests.post(f"{BOT_URL}/sendMessage", json={
                    "chat_id": ADMIN_CHAT_ID,
                    "text": f"🔔 Новый пользователь нажал /start\nИмя: {message['from'].get('first_name')} @{message['from'].get('username', '')}"
                })

            elif "language" in text or "язык" in text:
                send_message(chat_id, messages[lang]['choose_lang'], {
                    "inline_keyboard": [
                        [{"text": "🇷🇺 Русский", "callback_data": "set_lang_ru"}],
                        [{"text": "🇬🇧 English", "callback_data": "set_lang_en"}]
                    ]
                })

        elif 'location' in message:
            latitude = message['location']['latitude']
            longitude = message['location']['longitude']
            link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"

            requests.post(f"{BOT_URL}/sendMessage", json={
                "chat_id": ADMIN_CHAT_ID,
                "text": f"📍 Новый заказ!\nЛокация: {link}\nПользователь: @{message['from'].get('username', '')}"
            })

            send_message(chat_id, "✅ Заказ принят! Мы скоро с вами свяжемся. / Your request has been received!")

    elif "callback_query" in data:
        callback = data["callback_query"]
        chat_id = callback["from"]["id"]
        data_val = callback["data"]

        if data_val == "set_lang_ru":
            send_message(chat_id, messages["ru"]["welcome"], get_keyboard("ru"))
        elif data_val == "set_lang_en":
            send_message(chat_id, messages["en"]["welcome"], get_keyboard("en"))

    return {"ok": True}

def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)

    requests.post(f"{BOT_URL}/sendMessage", json=payload)

@app.route('/')
def index():
    return 'Telegram Bot Webhook Active!'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
