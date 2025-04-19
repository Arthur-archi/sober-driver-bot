import os
import csv
import logging
from flask import Flask, request
import requests

BOT_TOKEN = '8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA'
ADMIN_ID = '7465925576'
PHONE_NUMBER = '+971582615619'
WHATSAPP_LINK = f"https://wa.me/{PHONE_NUMBER.replace('+', '')}"

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def get_lang(message):
    lang = message.get("from", {}).get("language_code", "ru")
    return "en" if lang.startswith("en") else "ru"

def send_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(url, json=data)

def notify_admin(order_data):
    text = f"📥 Новый заказ от @{order_data['username']}\nИмя: {order_data['first_name']}\n"
    if order_data['location']:
        text += f"📍 Локация: https://www.google.com/maps?q={order_data['location']['latitude']},{order_data['location']['longitude']}"
    else:
        text += "Без геолокации."
    send_message(ADMIN_ID, text)

def save_order(order_data):
    file_exists = os.path.isfile("orders.csv")
    with open("orders.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["user_id", "username", "first_name", "location"])
        location_str = ""
        if order_data['location']:
            loc = order_data['location']
            location_str = f"{loc['latitude']},{loc['longitude']}"
        writer.writerow([
            order_data['user_id'],
            order_data['username'],
            order_data['first_name'],
            location_str
        ])

def create_buttons(lang):
    if lang == "en":
        text = "To order, send your location 📍 or press WhatsApp."
        call = "Call"
    else:
        text = "Чтобы заказать, отправьте свою геолокацию 📍 или нажмите на кнопку WhatsApp."
        call = "Позвонить"
    buttons = {
        "keyboard": [
            [{"text": "📍 Отправить локацию", "request_location": True}],
            [{"text": f"📞 {call}", "url": f"tel:{PHONE_NUMBER}"}],
            [{"text": "📱 WhatsApp", "url": WHATSAPP_LINK}]
        ],
        "resize_keyboard": True
    }
    return text, buttons

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    message = data.get("message") or data.get("edited_message")
    if not message:
        return "ok"

    chat_id = message["chat"]["id"]
    text = message.get("text", "").lower()
    user_id = message["from"]["id"]
    username = message["from"].get("username", "")
    first_name = message["from"].get("first_name", "")
    lang = get_lang(message)

    if message.get("location"):
        order_data = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "location": message["location"]
        }
        save_order(order_data)
        notify_admin(order_data)
        send_message(chat_id, "✅ Спасибо! Мы скоро свяжемся." if lang == "ru" else "✅ Thank you! We will contact you soon.")
        return "ok"

    if text == "/start":
        welcome = "🚗 Добро пожаловать!" if lang == "ru" else "🚗 Welcome!"
        send_message(chat_id, welcome)
        intro, markup = create_buttons(lang)
        send_message(chat_id, intro, reply_markup=markup)
    elif text == "/help":
        help_text = "Отправьте свою геолокацию или нажмите WhatsApp, чтобы сделать заказ." if lang == "ru" else "Send your location or press WhatsApp to place an order."
        send_message(chat_id, help_text)
    elif text == "/info":
        info = "Сервис 'Трезвый водитель' в Дубае. Мы доставим вас домой на вашей машине." if lang == "ru" else "‘Sober Driver’ service in Dubai. We’ll take you home in your car."
        send_message(chat_id, info)
    elif text == "/contact":
        contact = f"📞 {PHONE_NUMBER}\n📱 WhatsApp: {WHATSAPP_LINK}"
        send_message(chat_id, contact)
    elif text == "/order":
        order_data = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "location": None
        }
        save_order(order_data)
        notify_admin(order_data)
        send_message(chat_id, "✅ Спасибо! Мы скоро свяжемся." if lang == "ru" else "✅ Thank you! We will contact you soon.")
    else:
        default_text = "Напишите /help или отправьте геолокацию 📍" if lang == "ru" else "Type /help or send your location 📍"
        send_message(chat_id, default_text)
    return "ok"

@app.route('/')
def index():
    return "Bot is running!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
