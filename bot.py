from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import logging

BOT_TOKEN = "8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🧠 Память пользователей (user_id: lang)
user_languages = {}

# 📌 Языковые шаблоны
MESSAGES = {
    "ru": {
        "start": "👋 Добро пожаловать в сервис 'Трезвый водитель Дубай'!\n\nВыберите действие:",
        "help": "ℹ️ Это справка. Чтобы заказать водителя, нажмите /order.",
        "order": "🚗 Чтобы заказать водителя, нажмите кнопку 'Сделать заказ'.",
        "info": "ℹ️ Мы предоставляем услуги трезвого водителя в Дубае 24/7.",
        "contact": "📞 Наш номер: +971582615619\n📱 WhatsApp: https://wa.me/971582615619",
        "lang_set": "🇷🇺 Язык установлен на русский."
    },
    "en": {
        "start": "👋 Welcome to 'Sober Driver Dubai' service!\n\nPlease choose an option:",
        "help": "ℹ️ This is help. To order a driver, use /order.",
        "order": "🚗 To order a driver, press 'Make an order' button.",
        "info": "ℹ️ We provide sober driver services in Dubai 24/7.",
        "contact": "📞 Our number: +971582615619\n📱 WhatsApp: https://wa.me/971582615619",
        "lang_set": "🇬🇧 Language set to English."
    }
}

def get_lang(update: Update) -> str:
    user_id = update.effective_user.id
    return user_languages.get(user_id, "ru" if update.effective_user.language_code == "ru" else "en")

def main_menu_keyboard(lang: str):
    return ReplyKeyboardMarkup([
        [KeyboardButton("📍 Поделиться локацией", request_location=True)],
        [KeyboardButton("📞 Позвонить"), KeyboardButton("💬 WhatsApp")],
    ], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    await update.message.reply_text(
        MESSAGES[lang]["start"],
        reply_markup=main_menu_keyboard(lang)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    await update.message.reply_text(MESSAGES[lang]["help"])

async def order_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    await update.message.reply_text(MESSAGES[lang]["order"])

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    await update.message.reply_text(MESSAGES[lang]["info"])

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    await update.message.reply_text(MESSAGES[lang]["contact"])

# 🔁 Установка языка вручную
async def set_ru(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_languages[update.effective_user.id] = "ru"
    await update.message.reply_text(MESSAGES["ru"]["lang_set"])

async def set_en(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_languages[update.effective_user.id] = "en"
    await update.message.reply_text(MESSAGES["en"]["lang_set"])

async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    lat, lon = location.latitude, location.longitude
    maps_url = f"https://www.google.com/maps?q={lat},{lon}"
    await update.message.reply_text(f"📍 Спасибо! Ваша локация:\n{maps_url}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "Позвонить" in text or "Call" in text:
        await update.message.reply_text("📞 +971582615619")
    elif "WhatsApp" in text:
        await update.message.reply_text("💬 https://wa.me/971582615619")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("order", order_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CommandHandler("contact", contact_command))
    app.add_handler(CommandHandler("ru", set_ru))
    app.add_handler(CommandHandler("en", set_en))

    app.add_handler(MessageHandler(filters.LOCATION, location_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))

    print("🤖 Бот запущен с выбором языка!")
    app.run_polling()
