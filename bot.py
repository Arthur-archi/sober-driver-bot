from flask import Flask, request
import requests

# ✅ ТВОЙ ТОКЕН Telegram-бота
TOKEN = '8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}'

# ✅ Flask-приложение
app = Flask(__name__)

# ✅ Маршрут для webhook (POST)
@app.route('/', methods=['POST'])
def webhook():
    update = request.get_json()

    if 'message' in update:
        chat_id = update['message']['chat']['id']
        message = update['message'].get('text', '')

        reply_text = "🚗 Спасибо за заказ! Мы скоро с вами свяжемся.\n\n🇷🇺 Трезвый водитель Дубай\n🇬🇧 Sober Driver Dubai"

        # Отправка автоответа
        requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={
            'chat_id': chat_id,
            'text': reply_text
        })

    return {'ok': True}

# ✅ Проверочный маршрут (GET)
@app.route('/', methods=['GET'])
def index():
    return '✅ Бот "Трезвый водитель Дубай" работает!', 200

# ✅ Запуск сервера (для Railway)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
