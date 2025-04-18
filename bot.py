import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8099391152:AAG4UDErsqzn7cg7psJgcZEX_Hbb_5N8GcA"
ADMIN_ID = 7465925576

# Логгирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Автоответное сообщение
AUTO_REPLY = (
    "🚗 *Трезвый водитель Дубай*\n\n"
    "📍 Отправьте геолокацию для заказа.\n"
    "📞 Позвонить: +971582615619\n"
    "💬 WhatsApp: https://wa.me/971582615619\n"
)

# Приветствие
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("📍 Отправить геолокацию", request_location=True)],
        [KeyboardButton("📞 Позвонить"), KeyboardButton("💬 WhatsApp")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(AUTO_REPLY, reply_markup=reply_markup, parse_mode="Markdown")

# Обработка геолокации
async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    lat, lon = location.latitude, location.longitude
    user = update.message.from_user

    map_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

    # Сообщение пользователю
    await update.message.reply_text("✅ Заказ получен! Мы скоро свяжемся с вами.")
    
    # Сообщение администратору
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"📥 Новый заказ от @{user.username or user.first_name} (ID: {user.id})\n"
            f"🌍 Локация: {map_url}"
        )
    )

# Кнопка звонка и WhatsApp
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "позвонить" in text:
        await update.message.reply_text("📞 Звонок: +971582615619")
    elif "whatsapp" in text:
        await update.message.reply_text("💬 WhatsApp: https://wa.me/971582615619")

# Основной запуск
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, location_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("🤖 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
