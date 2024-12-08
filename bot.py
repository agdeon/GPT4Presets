import telebot
from telebot import types
import os

from user import User
from keyboard_button_manager import KeyBoardButtonManager

# Создайте объект бота с вашим токеном
TOKEN = os.getenv('agdeon_test_bot_telegram_api_key')  # Замените на свой токен
bot = telebot.TeleBot(TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = User(message.chat.id)
    button_manager = KeyBoardButtonManager(Event(bot, message, user))
    button_manager.create_menu()


# Обработчик нажатия на кнопку
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # bot.send_message(message.chat.id, f"Вы нажали {message.text}")
    user = User(message.chat.id)
    kb_manager = KeyBoardButtonManager(Event(bot, message, user))
    if kb_manager.is_keyboard_event():
        kb_manager.handle_keyboard_event()


# Запуск бота
bot.polling(none_stop=True)