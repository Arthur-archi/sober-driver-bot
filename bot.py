from flask import Flask, request
import telegram
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import os

# Твои данные
BOT_TOKEN = "8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA"
ADMIN_ID = 7465925576

bot = telegram.Bot(token=BOT_TOKEN)
app = Flask(__name__)


# Языковые сообщения
texts = {
    "start_ru": "🚘 <b>Трезвый водитель Дубай</b>\n\n📍 Мы доставим вас и ваш автомобиль в любую точку Дубая.\n📲 Нажмите кнопку ниже, чтобы поделиться геолокацией или связаться с нами.\n\n❓Если что-то непонятно — напишите администратору: @Arthur_01",
    "start_en": "🚘 <b>Sober Driver Dubai</b>\n\n📍 We will deliver you and your car anywhere in Dubai.\n📲 Press the button below to share your location or contact us.\n\n❓If something is unclear — contact the admin: @Arthur_01",

    "thanks_ru": "✅ Спасибо! Мы получили вашу геолокацию.\n\nПожалуйста, напишите:\n1️⃣ Адрес назначения (точка Б)\n2️⃣ Марку и модель автомобиля\n3️⃣ Номер машины (если есть)\n4️⃣ Контактный номер для связи\n5️⃣ Уточнения или пожелания (по времени, срочности и т.д.)",
    "thanks_en": "✅ Thank you! We received your location.\n\nPlease write:\n1️⃣ Destination address (point B)\n2️⃣ Car brand and model\n3️⃣ Car number (if any)\n4️⃣ Contact number\n5️⃣ Comments or wishes (urgency, time, etc.)",
}


def get_user_language(update: Update) -> str:
    lang_code = update.effective_user.language_code
    return "en" if lang_code == "en" else "ru"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_language(update)
    text = texts["start_en"] if lang == "en" else texts["start_ru"]

    keyboard = [
        [KeyboardButton("📍 Отправить геолокацию", request_location=True)],
        [KeyboardButton("📞 Позвонить"), KeyboardButton("💬 WhatsApp")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="HTML")


async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    lang = get_user_language(update)
    text = texts["thanks_en"] if lang == "en" else texts["thanks_ru"]

    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    location_link = f"https://www.google.com/maps?q={latitude},{longitude}"

    # Ответ клиенту
    await update.message.reply_text(text)

    # Уведомление админу
    admin_text = f"📍 Новый заказ от {user.first_name}\nСсылка на локацию: {location_link}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text)


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"📩 Ответ от {user.first_name}:\n{text}")


# Flask endpoint
@app.route('/webhook', methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    app.dispatcher.process_update(update)
    return "ok", 200


@app.route('/set_webhook')
def set_webhook():
    webhook_url = f"https://sober-driver-dubai.up.railway.app/webhook"
    success = bot.set_webhook(url=webhook_url)
    return {"ok": success}


# Telegram Application (async)
def start_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.LOCATION, location_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    return application


if __name__ == "__main__":
    telegram_app = start_bot()
    telegram_app.run_polling()
