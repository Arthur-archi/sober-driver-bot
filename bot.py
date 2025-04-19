from flask import Flask, request
import requests
import csv
from datetime import datetime

TOKEN = '8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA'
ADMIN_ID = '7465925576'
PHONE = '+971582615619'
WHATSAPP = 'https://wa.me/971582615619'

app = Flask(__name__)

def send_message(chat_id, text, reply_markup=None, parse_mode=None):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    if reply_markup:
        payload['reply_markup'] = reply_markup
    if parse_mode:
        payload['parse_mode'] = parse_mode
    requests.post(url, json=payload)

def get_keyboard(lang):
    if lang == 'ru':
        return {
            "keyboard": [
                [{"text": "📍 Отправить локацию", "request_location": True}],
                [{"text": f"📞 Позвонить: {PHONE}"}],
                [{"text": "💬 WhatsApp", "url": WHATSAPP}]
            ],
            "resize_keyboard": True
        }
    else:
        return {
            "keyboard": [
                [{"text": "📍 Send location", "request_location": True}],
                [{"text": f"📞 Call: {PHONE}"}],
                [{"text": "💬 WhatsApp", "url": WHATSAPP}]
            ],
            "resize_keyboard": True
        }

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' in data:
        msg = data['message']
        chat_id = msg['chat']['id']
        lang = msg.get('from', {}).get('language_code', 'en')
        lang = 'ru' if lang.startswith('ru') else 'en'

        if 'text' in msg and msg['text'] == '/start':
            text = "🚗 Добро пожаловать!" if lang == 'ru' else "🚗 Welcome!"
            send_message(chat_id, text, reply_markup=get_keyboard(lang))
        
        elif 'location' in msg:
            lat = msg['location']['latitude']
            lon = msg['location']['longitude']
            link = f"https://www.google.com/maps?q={lat},{lon}"
            thank = "Спасибо! Локация получена 📍" if lang == 'ru' else "Thanks! Location received 📍"
            send_message(chat_id, thank + f"\n\n<a href='{link}'>Открыть на карте</a>", parse_mode='HTML')
            send_message(ADMIN_ID, f"🚨 Новый заказ от ID {chat_id}\n<a href='{link}'>Открыть карту</a>", parse_mode='HTML')
            save_order(chat_id, lat, lon)

        else:
            msg_text = "✅ Спасибо! Мы скоро свяжемся." if lang == 'ru' else "✅ Thank you! We’ll contact you shortly."
            send_message(chat_id, msg_text)

    return 'ok'

@app.route('/', methods=['GET'])
def index():
    return 'Bot is running!'

def save_order(user_id, lat, lon):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('orders.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([now, user_id, lat, lon])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

