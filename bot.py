@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Получено:", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "").lower()

        if text == "/start":
            send_message(chat_id, "Привет! Это Трезвый водитель Дубай 🚘\n\nПомощь / Help")
        elif text == "/help":
            send_message(chat_id, "Список доступных команд:\n/order — Заказать\n/info — Инфо\n/contact — Контакты")
        elif text == "/order":
            send_message(chat_id, "Чтобы заказать, отправьте свою геолокацию или позвоните нам 📍📞")
        elif text == "/info":
            send_message(chat_id, "Мы предоставляем услугу 'трезвый водитель' в Дубае. Работаем 24/7.")
        elif text == "/contact":
            send_message(chat_id, "📞 Позвонить: +971582615619\n💬 WhatsApp: https://wa.me/971582615619")
        elif "language" in text or "язык" in text:
            send_message(chat_id, "Выберите язык:\n🇷🇺 Русский\n🇬🇧 English")
        else:
            send_message(chat_id, "Команда не распознана. Попробуйте /start или /help")

    return "OK", 200
