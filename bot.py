import json
import ssl
import urllib.request
import time

# 🔑 Токен и ID админа
TOKEN = "8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA"
ADMIN_ID = 7465925576  # Telegram ID администратора (Artur)

API_URL = f"https://api.telegram.org/bot{TOKEN}/"
ctx = ssl.create_default_context()

# 🧠 Память для выбора языка
user_languages = {}

def api(method, data=None):
    url = API_URL + method
    if data:
        data = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(url, data, headers={"Content-Type": "application/json"})
    else:
        req = urllib.request.Request(url)
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.load(r)

def get_updates(offset=None):
    return api("getUpdates", {"offset": offset, "timeout": 30})["result"]

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    api("sendMessage", data)

def get_language_code(message):
    chat_id = message["chat"]["id"]
    return user_languages.get(chat_id, "ru")

def get_welcome_message(lang):
    if lang == "ru":
        return (
            "🚘 <b>Трезвый водитель Дубай</b>\n\n"
            "📍 Мы доставим вас и ваш автомобиль в любую точку Дубая.\n"
            "📲 Нажмите кнопку ниже, чтобы поделиться геолокацией или связаться с нами.\n\n"
            "📞 Номер: +971582615619\n"
            "💬 WhatsApp: https://wa.me/971582615619\n"
            "❓ Вопросы? Напишите: @Arthur_01"
        )
    else:
        return (
            "🚘 <b>Sober Driver Dubai</b>\n\n"
            "📍 We will take you and your car anywhere in Dubai.\n"
            "📲 Tap a button below to share your location or contact us.\n\n"
            "📞 Phone: +971582615619\n"
            "💬 WhatsApp: https://wa.me/971582615619\n"
            "❓ Questions? Message us: @Arthur_01"
        )

def get_buttons(lang):
    if lang == "ru":
        return {
            "keyboard": [
                [{"text": "📍 Отправить геолокацию", "request_location": True}],
                [{"text": "📞 Позвонить"}, {"text": "💬 WhatsApp"}]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": False
        }
    else:
        return {
            "keyboard": [
                [{"text": "📍 Share Location", "request_location": True}],
                [{"text": "📞 Call"}, {"text": "💬 WhatsApp"}]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": False
        }

def handle_command(chat_id, text, lang):
    if text == "/start":
        reply_markup = {
            "keyboard": [[{"text": "🇷🇺 Русский"}, {"text": "🇬🇧 English"}]],
            "resize_keyboard": True,
            "one_time_keyboard": True
        }
        send_message(chat_id, "🌐 Выберите язык / Choose your language:", reply_markup)
        return

    if lang == "ru":
        responses = {
            "/help": "ℹ️ Чтобы заказать водителя, нажмите кнопку 'Отправить геолокацию'.",
            "/order": "🚗 Ваша заявка принята! Мы уже едем.",
            "/info": "📄 Мы работаем круглосуточно по всему Дубаю.",
            "/contact": "📞 Номер: +971582615619\n💬 WhatsApp: https://wa.me/971582615619"
        }
        unknown = "❌ Неизвестная команда. Пожалуйста, нажмите /start, чтобы начать."
    else:
        responses = {
            "/help": "ℹ️ To request a driver, click 'Share Location' below.",
            "/order": "🚗 Your order has been received! We're on the way.",
            "/info": "📄 We operate 24/7 all across Dubai.",
            "/contact": "📞 Phone: +971582615619\n💬 WhatsApp: https://wa.me/971582615619"
        }
        unknown = "❌ Unknown command. Please press /start to begin."

    response = responses.get(text)
    if response:
        send_message(chat_id, f"📩 {response}")
    else:
        send_message(chat_id, unknown)


def handle_text(chat_id, text, lang):
    if text == "🇷🇺 Русский":
        user_languages[chat_id] = "ru"
        send_message(chat_id, get_welcome_message("ru"), get_buttons("ru"))
        return
    elif text == "🇬🇧 English":
        user_languages[chat_id] = "en"
        send_message(chat_id, get_welcome_message("en"), get_buttons("en"))
        return

    text = text.lower()
    if "позвонить" in text or "call" in text:
        send_message(chat_id, "📞 +971582615619")
        return  # 👈 добавим return здесь
    elif "whatsapp" in text:
        send_message(chat_id, "💬 WhatsApp: https://wa.me/971582615619")
        return  # 👈 и здесь тоже

    message = (
        "🤖 Спасибо! Мы получили ваше сообщение.\n\n"
        "📍 Чтобы сделать заказ, нажмите кнопку “Отправить геолокацию” ниже\n"
        "или напишите нам напрямую: @Arthur_01"
        if lang == "ru" else
        "🤖 Thank you! We got your message.\n\n"
        "📍 To make a request, tap “Share Location” below or contact us at: @Arthur_01"
    )
    send_message(chat_id, message)


def handle_location(chat_id, location, lang):
    latitude = location["latitude"]
    longitude = location["longitude"]
    maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
    message = (
        f"📍 Спасибо! Мы получили вашу геолокацию.\n<a href='{maps_url}'>Открыть в Google Maps</a>"
        if lang == "ru" else
        f"📍 Thank you! We received your location.\n<a href='{maps_url}'>Open in Google Maps</a>"
    )
    send_message(chat_id, message)
    send_message(ADMIN_ID, f"📍 Новый заказ!\nКоординаты: {latitude}, {longitude}\n{maps_url}")

def main():
    offset = None
    print("✅ Бот запущен")
    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            message = update.get("message")
            if not message:
                continue

            chat_id = message["chat"]["id"]
            lang = get_language_code(message)

            if "text" in message:
                text = message["text"]
                if text.startswith("/"):
                    handle_command(chat_id, text, lang)
                else:
                    handle_text(chat_id, text, lang)

            elif "location" in message:
                handle_location(chat_id, message["location"], lang)

        time.sleep(1)

if __name__ == "__main__":
    main()
