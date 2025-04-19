from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = '8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA'
API_URL = f'https://api.telegram.org/bot{TOKEN}'
ADMIN_ID = '7465925576'

@app.route('/', methods=['GET'])
def index():
    return '✅ Бот работает!', 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if 'message' in data:
        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')

        # Ответ пользователю
        requests.post(f"{API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": "🚗 Спасибо! Мы получили ваш запрос и скоро свяжемся.\n🇷🇺 Трезвый водитель Дубай / 🇬🇧 Sober Driver Dubai"
        })

        # Уведомление админа
        requests.post(f"{API_URL}/sendMessage", json={
            "chat_id": ADMIN_ID,
            "text": f"📦 Новый запрос от пользователя:\n{text}"
        })

    return {'ok': True}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

