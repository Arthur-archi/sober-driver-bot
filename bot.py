import os
import flask
import requests
from flask import request

TOKEN = '8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA'
URL = f'https://api.telegram.org/bot{TOKEN}'
ADMIN_CHAT_ID = '7465925576'  # ID Артура

app = flask.Flask(__name__)

# Хранилище языков пользователей
user_languages = {}

# Команды на двух языках
MESSAGES = {
    'ru': {
        'start': "👋 Добро пожаловать в сервис «Трезвый водитель Дубай»!\n\n📍 Мы доставим вас и ваш автомобиль в любую точку Дубая.\n📲 Нажмите кнопку ниже, чтобы поделиться геолокацией или связаться с нами.\n\n❓ Если что-то непонятно — напишите администратору: @Arthur_01",
        'language': "Выберите язык / Choose your language:",
        'help': "ℹ️ Напишите /order чтобы сделать заказ.\n📍 Отправьте свою геолокацию для вызова водителя.",
        'order': "🚘 Для заказа нажмите кнопку 'Отправить местоположение' или напишите нам в WhatsApp.",
        'info': "ℹ️ Сервис работает круглосуточно по всему Дубаю.",
        'contact': "📞 WhatsApp: +971582615619\n👤 Администратор: @Arthur_01"
    },
    'en': {
        'start': "👋 Welcome to 'Sober Driver Dubai' service!\n\n📍 We will deliver you and your car anywhere in Dubai.\n📲 Press the button below to share your location or contact us.\n\n❓ If anything is unclear — contact admin: @Arthur_01",
        'language': "Choose your language / Выберите язык:",
        'help': "ℹ️ Type /order to place an order.\n📍 Send your location to request a driver.",
        'order': "🚘 To order, press 'Send Location' or contact us on WhatsApp.",
        'info': "ℹ️ We work 24/7 all around Dubai.",
        'contact': "📞 WhatsApp: +971582615619\n👤 Admin: @Arthur_01"
    }
}

def send_message(chat_id, text, reply_markup=None):
    data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    if reply_markup:
        data['reply_markup'] = reply_markup
    requests.post(f'{URL}/sendMessage', json=data)

def get_language(user_id):
    return user_languages.get(user_id, 'ru')

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = request.get_json()

    if 'message' in update:
        message = update['message']
        chat_id = message['chat']['id']
        user_id = message['from']['id']
        text = message.get('text', '')
        
        if text == '/start':
            lang_keyboard = {
                "keyboard": [
                    [{"text": "🇷🇺 Русский"}, {"text": "🇬🇧 English"}]
                ],
                "resize_keyboard": True
            }
            send_message(chat_id, MESSAGES['ru']['language'], reply_markup=lang_keyboard)
            return 'ok'

        elif text in ['🇷🇺 Русский', '🇬🇧 English']:
            lang = 'ru' if 'Русский' in text else 'en'
            user_languages[user_id] = lang
            send_message(chat_id, MESSAGES[lang]['start'])
            return 'ok'

        elif text in ['/help', '/order', '/info', '/contact']:
            lang = get_language(user_id)
            command = text.replace('/', '')
            send_message(chat_id, MESSAGES[lang].get(command, ''))
            return 'ok'

        elif 'location' in message:
            send_message(ADMIN_CHAT_ID, f"📍 Новый заказ! Локация:\nhttps://maps.google.com/?q={message['location']['latitude']},{message['location']['longitude']}")
            send_message(chat_id, "✅ Локация получена! Водитель скоро будет с вами. / Location received! Driver is on the way.")
            return 'ok'

    return 'ok'

@app.route('/')
def index():
    return 'Сервис работает!'

if __name__ == '__main__':
    app.run()
