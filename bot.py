import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = '8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA'
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'
ADMIN_ID = '7465925576'

CALLBACK_BUTTONS = {
    "share_location": {
        "ru": "📍 Отправить геолокацию",
        "en": "📍 Share location"
    },
    "call": {
        "ru": "📞 Позвонить",
        "en": "📞 Call"
    },
    "whatsapp": {
        "ru": "💬 WhatsApp",
        "en": "💬 WhatsApp"
    }
}


def send_message(chat_id, text, reply_markup=None):
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    if reply_markup:
        payload['reply_markup'] = reply_markup
    requests.post(f"{API_URL}/sendMessage", json=payload)


def detect_language(lang_code):
    return 'ru' if lang_code.startswith('ru') else 'en'


def build_keyboard(language):
    return {
        "keyboard": [
            [{"text": CALLBACK_BUTTONS["share_location"][language], "request_location": True}],
            [{"text": CALLBACK_BUTTONS["call"][language], "url": "tel:+971582615619"}],
            [{"text": CALLBACK_BUTTONS["whatsapp"][language], "url": "https://wa.me/971582615619"}],
        ],
        "resize_keyboard": True
    }


def create_route_link(latitude, longitude):
    return f"https://www.google.com/maps?q={latitude},{longitude}"


@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()

    if 'message' in data:
        message = data['message']
        chat_id = message['chat']['id']
        user_lang = detect_language(message['from'].get('language_code', 'en'))

        if 'location' in message:
            lat = message['location']['latitude']
            lon = message['location']['longitude']
            route_link = create_route_link(lat, lon)

            confirmation_text = {
                "ru": f"✅ Ваш заказ принят!\n📍 <a href='{route_link}'>Маршрут</a>\n⏳ Ожидайте водителя!",
                "en": f"✅ Your order has been accepted!\n📍 <a href='{route_link}'>Route</a>\n⏳ Please wait for the driver!"
            }

            admin_text = f"📬 Новый заказ!\n🌍 <a href='{route_link}'>Геолокация клиента</a>\n👤 @{message['from'].get('username', 'Без username')}"
            send_message(chat_id, confirmation_text[user_lang])
            send_message(ADMIN_ID, admin_text)

        else:
            welcome_text = {
                "ru": (
                    "👋 Добро пожаловать в сервис 'Трезвый водитель Дубай'!\n\n"
                    "🚗 Трезвый водитель Дубай\n📍 Мы доставим вас и ваш автомобиль в любую точку Дубая.\n"
                    "📲 Поделитесь геолокацией или нажмите кнопку для связи.\n"
                    "❓ Если возникли вопросы — напишите администратору: @Arthur_01"
                ),
                "en": (
                    "👋 Welcome to 'Sober Driver Dubai' service!\n\n"
                    "🚗 Sober Driver Dubai\n📍 We will drive you and your car anywhere in Dubai.\n"
                    "📲 Share your location or click a button below to contact us.\n"
                    "❓ For questions — contact the admin: @Arthur_01"
                )
            }

            send_message(chat_id, welcome_text[user_lang], reply_markup=build_keyboard(user_lang))

    return {'ok': True}


# Установка webhook (выполняется один раз локально или вручную)
@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    webhook_url = f"https://sober-driver-dubai.up.railway.app/{BOT_TOKEN}"
    response = requests.get(f"{API_URL}/setWebhook?url={webhook_url}")
    return response.json()


if __name__ == "__main__":
    app.run()
