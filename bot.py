import os
import flask
import requests
from flask import request

# === Настройки ===
TOKEN = '8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA'
URL = f'https://api.telegram.org/bot{TOKEN}'
ADMIN_CHAT_ID = '7465925576'

app = flask.Flask(__name__)

# Хранилище выбранных языков
user_languages = {}

# Шаблоны сообщений
MESSAGES = {
    'ru': {
        'start': "👋 Добро пожаловать в сервис «Трезвый водитель Дубай»!\n\n📍 Мы доставим вас и ваш автомобиль в любую точку Дубая.\n📲 Нажмите кнопку ниже, чтобы поделиться геолокацией или связаться с нами.\n\n❓ Вопросы? Напишите администратору: @Arthur_01",
        'language': "Выберите язык / Choose your language:",
        'help': "ℹ️ Используйте /order для заказа или отправьте геолокацию.",
        'order': "🚘 Нажмите '📍 Отправить геолокацию' или напишите нам в WhatsApp.",
        'info': "ℹ️ Мы работаем 24/7 по всему Дубаю.",
        'contact': "📞 WhatsApp: +971582615619\n👤 Админ: @Arthur_01"
    },
    'en': {
        'start': "👋 Welcome to 'Sober Driver Dubai' service!\n\n📍 We will drive you and your car anywhere in Dubai.\n📲 Press the button below to share your location or contact us.\n\n❓ Questions? Message the admin: @Arthur_01",
        'language': "Choose your language / Выберите язык:",
        'help': "ℹ️ Use /order to request a driver or send your location.",
        'order': "🚘 Press '📍 Send location' or contact us on WhatsApp.",
        'info': "ℹ️ We operate 24/7 all over Dubai.",
        'contact': "📞 WhatsApp: +971582615619\n👤 Admin: @Arthur_01"
    }
}

# === Универсальная отправка сообщений ===
def send_message(chat_id, text, reply_markup=None):
    data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    if reply_markup:
        data['reply_markup'] = reply_markup
    requests.post(f'{URL}/sendMessage', json=data)

# === Определение языка пользователя ===
def get_language(user_id):
    return user_languages.get(user_id, 'ru')

# === ВНИМАНИЕ: ЖЁСТКИЙ Webhook маршрут (БЕЗ {TOKEN}) ===
@app.route('/8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA', methods=['POST'])
def webhook():
    update = request.get_json()

    if 'message' in update:
        message = update['message']
        chat_id = message['chat']['id']
        user_id = message['from']['id']
        text = message.get('text', '')

        # Команда /start
        if text == '/start':
            lang_keyboard = {
                "keyboard": [
                    [{"text": "🇷🇺 Русский"}, {"text": "🇬🇧 English"}]
                ],
                "resize_keyboard": True
            }
            send_message(chat_id, MESSAGES['ru']['language'], reply_markup=lang_keyboard)
            return 'ok'

        # Выбор языка
        elif text in ['🇷🇺 Русский', '🇷🇺']:
            user_languages[user_id] = 'ru'
            send_message(chat_id, MESSAGES['ru']['start'])
            return 'ok'
        elif text in ['🇬🇧 English', '🇬🇧']:
            user_languages[user_id] = 'en'
            send_message(chat_id, MESSAGES['en']['start'])
            return 'ok'

        lang = get_language(user_id)

        # Команды
        if text in ['/help', '/order', '/info', '/contact']:
            command = text.replace('/', '')
            send_message(chat_id, MESSAGES[lang].get(command, ''))
            return 'ok'

        # Геолокация
        if 'location' in message:
            location = message['location']
            maps_link = f"https://maps.google.com/?q={location['latitude']},{location['longitude']}"

            send_message(ADMIN_CHAT_ID, f"📍 Новый заказ от @{message['from'].get('username', '')}\nЛокация: {maps_link}")
            send_message(chat_id, "✅ Локация получена! Водитель выехал." if lang == 'ru' else "✅ Location received! Driver is on the way.")
            return 'ok'

        # Иные сообщения
        send_message(chat_id, MESSAGES[lang]['help'])
        return 'ok'

    return 'ok'

# Проверка доступности
@app.route('/')
def index():
    return '🟢 Бот работает!'

if __name__ == '__main__':
    app.run()

