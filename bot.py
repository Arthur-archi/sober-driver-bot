import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackContext
import asyncio
import os

# === НАСТРОЙКИ ===
BOT_TOKEN = "8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA"
ADMIN_CHAT_ID = 7465925576
PHONE_NUMBER = "+971582615619"
WHATSAPP_LINK = "https://wa.me/971582615619"

# === ЛОГГИРОВАНИЕ ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === ЯЗЫКОВЫЕ ТЕКСТЫ ===
TEXTS = {
    "ru": {
        "start": "🚗 Добро пожаловать в сервис *Трезвый водитель Дубай*!\n\n📍 Мы доставим вас и ваш автомобиль в любую точку Дубая.\n\nВыберите действие ниже 👇",
        "location_button": "📍 Отправить локацию",
        "call_button": "📞 Позвонить",
        "whatsapp_button": "💬 WhatsApp",
        "confirm": "✅ Спасибо! Мы получили ваш заказ. Водитель скоро свяжется с вами.",
        "admin_msg": "📥 Новый заказ:\nИмя: {name}\nUsername: @{username}\nЛокация: https://maps.google.com/?q={lat},{lon}",
    },
    "en": {
        "start": "🚗 Welcome to *Sober Driver Dubai*!\n\n📍 We will drive you and your car anywhere in Dubai.\n\nChoose an action below 👇",
        "location_button": "📍 Send Location",
        "call_button": "📞 Call",
        "whatsapp_button": "💬 WhatsApp",
        "confirm": "✅ Thank you! We received your order. The driver will contact you soon.",
        "admin_msg": "📥 New order:\nName: {name}\nUsername: @{username}\nLocation: https://maps.google.com/?q={lat},{lon}",
    }
}

# === ОПРЕДЕЛЕНИЕ ЯЗЫКА ===
def get_lang(update: Update) -> str:
    user_lang = update.effective_user.language_code
    return "ru" if user_lang == "ru" else "en"

# === СТАРТ ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    t = TEXTS[lang]

    keyboard = [
        [KeyboardButton(t["location_button"], request_location=True)],
        [KeyboardButton(t["call_button"]), KeyboardButton(t["whatsapp_button"])]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(t["start"], reply_markup=reply_markup, parse_mode="Markdown")

# === ОБРАБОТКА ЛОКАЦИИ ===
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    t = TEXTS[lang]

    location = update.message.location
    user = update.message.from_user

    admin_message = t["admin_msg"].format(
        name=user.full_name,
        username=user.username or "без username",
        lat=location.latitude,
        lon=location.longitude,
    )

    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)
    await update.message.reply_text(t["confirm"], reply_markup=ReplyKeyboardRemove())

# === ОБРАБОТКА КНОПОК ===
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    t = TEXTS[lang]
    text = update.message.text

    if t["call_button"] in text:
        await update.message.reply_text(f"📞 Позвонить: {PHONE_NUMBER}")
    elif t["whatsapp_button"] in text:
        await update.message.reply_text(f"💬 WhatsApp: {WHATSAPP_LINK}")
    else:
        await start(update, context)

# === ОСНОВНАЯ ФУНКЦИЯ ===
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

