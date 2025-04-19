from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA"
ADMIN_ID = 7465925576
PHONE = "+971582615619"
WHATSAPP_URL = "https://wa.me/971582615619"
API_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text}
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(f"{API_URL}/sendMessage", json=data)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "").lower()

        if text == "/start":
            keyboard = {
                "keyboard": [
                    ["/order", "/info"],
                    ["/contact", "🌐 Language / Язык"],
                    ["📍 Отправить геолокацию / Share Location"]
                ],
                "resize_keyboard": True
            }
            send_message(chat_id, "Привет! Это Трезвый водитель Дубай 🚘", reply_markup=keyboard)
        elif text == "/order":
            send_message(chat_id, "Чтобы заказать, отправьте свою геолокацию 📍 или нажмите на кнопку WhatsApp.")
        elif text == "/info":
            send_message(chat_id, "🚘 Мы предлагаем услугу 'Трезвый водитель' в Дубае 24/7.")
        elif text == "/contact":
            send_message(chat_id, f"📞 {PHONE}\n💬 {WHATSAPP_URL}")
        elif "language" in text or "язык" in text:
            send_message(chat_id, "🇷🇺 Русский / 🇬🇧 English coming soon")
        else:
            send_message(chat_id, "Команда не распознана. Напишите /start")

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
