from flask import Flask, request
import requests
import json

TOKEN = '8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/'
ADMIN_ID = '7465925576'

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        
        # Пример ответа
        if text == '/start':
            send_message(chat_id, "Привет! Это Трезвый водитель Дубай 🚘")
        elif text == '/help':
            send_message(chat_id, "Помощь / Help")
        else:
            send_message(chat_id, "Команда не распознана. Попробуйте /start или /help")

    return '', 200

def send_message(chat_id, text):
    url = TELEGRAM_API_URL + 'sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
