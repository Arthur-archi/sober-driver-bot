import logging
from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
import os

# ТВОИ ДАННЫЕ
BOT_TOKEN = "8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA"
ADMIN_ID = 7465925576

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# СООБЩЕНИЯ
TEXTS = {
    "ru": {
        "start": (
            "🚘 <b>Трезвый водитель Дубай</b>\n\n"
            "📍 Мы доставим вас и ваш автомобиль в любую точку Дубая.\n"
            "📲 Поделитесь геолокацией или нажмите кнопку для связи.\n\n"
            "❓ Если возникли вопросы — напишите администратору: @Arthur_01"
        ),
        "thanks": (
            "✅ Спасибо! Мы получили вашу геолокацию.\n\n"
            "Пожалуйста, напишите:\n"
            "1️⃣ Адрес назначения\n"
            "2️⃣ Марку и модель авто\n"
            "3️⃣ Номер машины (если есть)\n"
            "4️⃣ Контактный номер\n"
            "5️⃣ Пожелания (время, срочность и т.д.)"
        ),
        "received": "📩 Ваше сообщение отправлено. Мы скоро с вами свяжемся.",
    },
    "en": {
        "start": (
            "🚘 <b>Sober Driver Dubai</b>\n\n"
            "📍 We will drive you and your car anywhere in Dubai.\n"
            "📲 Share your location or use the buttons below to contact us.\n\n"
            "❓ Have questions? Contact the admin: @Arthur_01"
        ),
        "thanks": (
            "✅ Thank you! We have received your location.\n\n"
            "Please send us:\n"
            "1️⃣ Destination address\n"
            "2️⃣ Car make and model\n"
            "3️⃣ Car plate (if any)\n"
            "4️⃣ Your contact number\n"
            "5️⃣ Any notes (time, urgency, etc.)"
        ),
        "received": "📩 Your message has been forwarded. We will contact you soon.",
    },
}

# Определение языка
def get_lang(update: Update) -> str:
    user_lang = update.effective_user.language_code
    return "ru" if user_lang == "ru" else "en"

# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    text = TEXTS[lang]["start"]
    keyboard = [
        [KeyboardButton("📍 Отправить геолокацию", request_location=True)],
        [KeyboardButton("📞 Позвонить"), KeyboardButton("💬 WhatsApp")],
    ]
    await update.message.reply_text(
        text=text,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode="HTML"
    )

# Геолокация
async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loc = update.message.location
    lang = get_lang(update)
    link = f"https://www.google.com/maps?q={loc.latitude},{loc.longitude}"
    name = update.effective_user.first_name

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=TEXTS[lang]["thanks"]
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📍 Новый заказ от {name}\n{link}"
    )

# Текстовые сообщения
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    name = update.effective_user.first_name
    text = update.message.text

    if "Позвонить" in text or "Call" in text:
        await update.message.reply_text("📞 Звоните: +971582615619")

    elif "WhatsApp" in text:
        await update.message.reply_text("💬 WhatsApp: https://wa.me/971582615619")

    else:
        await update.message.reply_text(TEXTS[lang]["received"])
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 Сообщение от {name}:\n{text}"
        )

# Запуск
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, location))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
