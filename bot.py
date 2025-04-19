from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA"
API_URL = f"https://api.telegram.org/bot{TOKEN}"
ADMIN_ID = "7465925576"

@app.route('/', methods=['GET'])
def index():
    return "✅ Бот запущен и готов принимать Webhook!", 200

@app.route('/', methods=['POST'])
def webhook():
    update = request.get_json()

    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "🚘 Новый запрос без текста")

        # Ответ клиенту
        requests.post(f"{API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": "✅ Ваш запрос получен! Мы скоро свяжемся с вами.\n\n🚗 Трезвый водитель Дубай"
        })

        # Уведомление админу
        requests.post(f"{API_URL}/sendMessage", json={
            "chat_id": ADMIN_ID,
            "text": f"📥 Новый заказ:\n{text}"
        })

    return {"ok": True}, 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
