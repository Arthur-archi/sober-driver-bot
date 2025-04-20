import json
import logging
import os
from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# === НАСТРОЙКИ ===
BOT_TOKEN = "8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA"
ADMIN_ID = 7465925576
PHONE_NUMBER = "+971582615619"
WHATSAPP_LINK = "https://wa.me/971582615619"
ORDERS_FILE = "orders.json"

# === ЛОГИ ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === ТЕКСТЫ ===
TEXTS = {
    "ru": {
        "welcome": "👋 Добро пожаловать в сервис *Трезвый водитель Дубай*!\n\nНажмите кнопку ниже, чтобы отправить свою геолокацию и оформить заказ.",
        "send_location": "📍 Отправьте свою геолокацию",
        "confirm": "✅ Заказ принят! Водитель скоро будет. Мы свяжемся с вами.",
        "admin_notify": "🚗 Новый заказ!\n\nИмя: {name}\nЯзык: Русский\nКоординаты: {location}\nСсылка: {map_url}",
    },
    "en": {
        "welcome": "👋 Welcome to *Sober Driver Dubai* service!\n\nClick the button below to share your location and place an order.",
        "send_location": "📍 Send your location",
        "confirm": "✅ Order confirmed! A driver is on the way. We will contact you shortly.",
        "admin_notify": "🚗 New Order!\n\nName: {name}\nLanguage: English\nLocation: {location}\nMap: {map_url}",
    }
}


def get_user_language(update: Update) -> str:
    return "ru" if update.effective_user.language_code == "ru" else "en"


def get_main_buttons(lang):
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(TEXTS[lang]["send_location"], request_location=True)],
            [KeyboardButton("📞 Позвонить" if lang == "ru" else "📞 Call")],
            [KeyboardButton("💬 WhatsApp")],
        ],
        resize_keyboard=True
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_language(update)
    text = TEXTS[lang]["welcome"]
    buttons = get_main_buttons(lang)
    await update.message.reply_text(text, reply_markup=buttons, parse_mode="Markdown")


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_user_language(update)
    location = update.message.location
    coords = f"{location.latitude}, {location.longitude}"
    map_url = f"https://www.google.com/maps?q={coords}"

    await update.message.reply_text(TEXTS[lang]["confirm"], reply_markup=ReplyKeyboardRemove())

    notify = TEXTS[lang]["admin_notify"].format(
        name=user.full_name,
        location=coords,
        map_url=map_url,
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=notify)

    save_order({
        "user_id": user.id,
        "name": user.full_name,
        "language": lang,
        "location": coords,
        "map_url": map_url
    })


def save_order(order_data):
    try:
        if os.path.exists(ORDERS_FILE):
            with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
        data.append(order_data)
        with open(ORDERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Ошибка при сохранении заказа: {e}")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    lang = get_user_language(update)

    if "whatsapp" in text:
        await update.message.reply_text(f"💬 WhatsApp: {WHATSAPP_LINK}")
    elif "позвонить" in text or "call" in text:
        await update.message.reply_text(f"📞 Телефон: {PHONE_NUMBER}")
    elif "сделать заказ" in text or "order" in text:
        await start(update, context)
    else:
        await update.message.reply_text(TEXTS[lang]["send_location"])


# === ЗАПУСК ===

from telegram.ext import Application
import asyncio

async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    await app.initialize()
    await app.start()
    logger.info("Бот запущен")
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
