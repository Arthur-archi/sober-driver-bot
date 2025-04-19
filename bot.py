from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = '8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA'
ADMIN_ID = '7465925576'

URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

# Определение языка по Telegram-настройкам
def detect_language(lang_code):
    if lang_code.startswith('ru'):
        return 'ru'
    return 'en'

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        lang_code = data['message']['from'].get('language_code', 'en')
        language = detect_language(lang_code)

        # Сообщения для пользователя
        if language == 'ru':
            text = "🚘 Добро пожаловать в сервис 'Трезвый водитель – Дубай'!\n\n📍 Отправьте геолокацию\n📞 Позвонить: +971582615619\n💬 WhatsApp: wa.me/971582615619"
        else:
            text = "🚘 Welcome to 'Sober Driver – Dubai'!\n\n📍 Send your location\n📞 Call: +971582615619\n💬 WhatsApp: wa.me/971582615619"

        requests.post(URL, json={"chat_id": chat_id, "text": text})

        # Уведомление администратору
        user_name = data['message']['from'].get('username', 'Без имени')
        message_text = data['message'].get('text', '[нет текста]')
        admin_text = f"📨 Новый заказ от @{user_name}\n📍 Сообщение: {message_text}"
        requests.post(URL, json={"chat_id": ADMIN_ID, "text": admin_text})

    return {'ok': True}

@app.route('/', methods=['GET'])
def index():
    return 'Бот работает!'

