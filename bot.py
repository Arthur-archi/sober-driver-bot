import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
PHONE = os.getenv("PHONE")
ORDERS_FILE = os.getenv("ORDERS_FILE", "orders.json")
RAILWAY_DOMAIN = os.getenv("RAILWAY_DOMAIN")
API_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    requests.post(f"{API_URL}/sendMessage", data=data)

def save_order(data):
    orders = []
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r", encoding="utf-8") as file:
            try:
                orders = json.load(file)
            except json.JSONDecodeError:
                pass
    orders.append(data)
    with open(ORDERS_FILE, "w", encoding="utf-8") as file:
        json.dump(orders, file, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return "Bot is running on Railway!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        user = update["message"]["from"]
        message = update["message"]
        text = message.get("text", "")
        location = message.get("location")

        # Язык
        lang = user.get("language_code", "ru")

        # Команды
        if text in ["/start", "/help"]:
            welcome = "Привет! Это Трезвый водитель Дубай 🚗" if lang.startswith("ru") else "Hi! This is Sober Driver Dubai 🚗"
            buttons = {
                "keyboard": [
                    [{"text": "📍 Отправить геолокацию / Share Location", "request_location": True}],
                    [{"text": f"📞 Позвонить / Call", "url": f"tel:{PHONE}"}],
                    [{"text": f"💬 WhatsApp", "url": f"https://wa.me/{PHONE.replace('+', '')}"}]
                ],
                "resize_keyboard": True
            }
            send_message(chat_id, welcome, buttons)

        elif text == "/order":
            info = "Пожалуйста, отправьте свою геолокацию 📍" if lang.startswith("ru") else "Please send your location 📍"
            send_message(chat_id, info)

        elif location:
            lat = location["latitude"]
            lon = location["longitude"]
            maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            confirm = "Спасибо! Ваш заказ принят. Мы скоро свяжемся с вами. ✅" if lang.startswith("ru") else "Thank you! Your order is confirmed. We'll contact you shortly. ✅"
            send_message(chat_id, confirm)
            order_data = {
                "user": f"{user.get('first_name')} {user.get('last_name', '')}",
                "username": user.get("username"),
                "location": {"latitude": lat, "longitude": lon},
                "maps_url": maps_url,
                "language": lang,
                "user_id": chat_id
            }
            save_order(order_data)
            # Отправка админу
            admin_text = f"📨 Новый заказ:\n👤 {order_data['user']}\n🌐 @{order_data['username']}\n📍 <a href='{maps_url}'>Открыть карту</a>"
            send_message(ADMIN_ID, admin_text)

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
