import telebot
from telebot import types
import os

from user import User
from button_manager import ButtonManager

# Создайте объект бота с вашим токеном
TOKEN = os.getenv('agdeon_test_bot_telegram_api_key')  # Замените на свой токен
bot = telebot.TeleBot(TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем клавиатуру
    user = User(message.chat.id)
    button_manager = ButtonManager(user)
    menu_markup = button_manager.create_menu()

    # Отправляем приветственное сообщение с кнопками
    bot.send_message(message.chat.id, "Привет! Выберите кнопку:", reply_markup=menu_markup)


# Обработчик нажатия на кнопку
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "☰ Скрыть меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton("☰ Открыть меню"))
        bot.send_message(message.chat.id, "Кнопки удалены!", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f"Вы нажали {message.text}")


# Запуск бота
bot.polling(none_stop=True)