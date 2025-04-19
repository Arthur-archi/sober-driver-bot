from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return '✅ Бот запущен (GET)', 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("📩 Пришёл POST-запрос от Telegram:")
    print(data)

    # Подтверждаем Telegram, что всё ОК
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
