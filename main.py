import telebot
import time

# Твой токен и айди
TOKEN = "8210304224:AAHFympd0qBtg65YSL08_i8Pa5WxZXsCI_I"
CHAT_ID = 5172658362  # твой id

bot = telebot.TeleBot(TOKEN)

# Команда /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Бот запущен ✅ и работает 24/7 (если на сервере)")

# Любое текстовое сообщение
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"Ты написал: {message.text}")

# Отправка авто-сообщений каждые 10 секунд
def auto_messages():
    while True:
        try:
            bot.send_message(CHAT_ID, "Я на связи 🔥")
        except Exception as e:
            print("Ошибка:", e)
        time.sleep(10)

import threading
threading.Thread(target=auto_messages, daemon=True).start()

print("Бот запущен...")
bot.infinity_polling()
