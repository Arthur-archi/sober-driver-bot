import logging
import asyncio
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA"
ADMIN_ID = 7465925576

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.effective_user.language_code
    user_id = update.effective_user.id

    ru_buttons = [
        [KeyboardButton("📍 Отправить геолокацию", request_location=True)],
        [KeyboardButton("📞 Позвонить"), KeyboardButton("💬 WhatsApp")],
        [KeyboardButton("🚗 Сделать заказ")]
    ]
    en_buttons = [
        [KeyboardButton("📍 Send location", request_location=True)],
        [KeyboardButton("📞 Call"), KeyboardButton("💬 WhatsApp")],
        [KeyboardButton("🚗 Make an order")]
    ]
    reply_markup = ReplyKeyboardMarkup(ru_buttons if lang == "ru" else en_buttons, resize_keyboard=True)

    text = "Привет! Я бот сервиса 'Трезвый водитель' в Дубае.\nВыберите действие ниже 👇" if lang == "ru" else \
           "Hi! I'm the 'Sober Driver' service bot in Dubai.\nPlease choose an action below 👇"

    await update.message.reply_text(text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    lang = user.language_code

    if text in ["📍 Отправить геолокацию", "📍 Send location"]:
        await update.message.reply_text("Пожалуйста, отправьте свою геолокацию 📍" if lang == "ru" else "Please send your location 📍")

    elif text in ["📞 Позвонить", "📞 Call"]:
        await update.message.reply_text("Позвоните нам: 📞 +971 58 261 5619")

    elif text in ["💬 WhatsApp"]:
        await update.message.reply_text("Напишите нам в WhatsApp:\nhttps://wa.me/971582615619")

    elif text in ["🚗 Сделать заказ", "🚗 Make an order"]:
        await update.message.reply_text("Ваш заказ принят! Мы свяжемся с вами в ближайшее время. ✅" if lang == "ru" else "Your request has been received! We’ll contact you shortly. ✅")
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"📥 Новый заказ от пользователя @{user.username} (ID: {user.id})")

    else:
        await update.message.reply_text("Я вас не понял. Пожалуйста, выберите кнопку ниже." if lang == "ru" else "I didn’t understand. Please use the buttons below.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

