from user import User
from user_interaction_handler import UIHandler
import json
import telebot
from telebot import types
from user_interaction_handler import UserEvent


class KeyboardButton:
    def __init__(self, text, callback):
        self.text = text
        self.callback = callback


class KeyBoardButtonManager:
    """
        Статичное меню
        💬 Обычный GPT
        🟢 Включить контекст
        📑 Выбрать пресет
        ➕ Создать пресет
        🗑 Удалить пресет
        📊 Мой профиль
    """

    # Все markup кнопки будут идентифицироваться по emoji
    # PRESET_INFO_BUTTON_ID = '💬' # у этой кнопки будет динамическое название в зависимости от пресета
    #
    # ENABLE_CONTEXT_BUTTON_ID = '🟢' # кнопки контекста будут сменяться одна на другую
    # ENABLE_CNTXT_B_TEXT = "Включить контекст"
    #
    # DISABLE_CONTEXT_BUTTON_ID = '🔴' # кнопки контекста будут сменяться одна на другую
    # DISABLE_CNTXT_B_TEXT = "Выключить контекст"
    #
    # CHOOSE_PRESET_BUTTON_ID = '📑'
    # CHOOSE_PRESET_B_TEXT = 'Выбрать пресет'
    #
    # CREATE_PRESET_BUTTON_ID = '➕'
    # CREATE_PRESET_B_TEXT = 'Создать пресет'
    #
    # REMOVE_PRESET_BUTTON_ID = '🗑️'
    # REMOVE_PRESET_B_TEXT = 'Удалить пресет'
    #
    # STAT_BUTTON_ID = '📊'
    # STAT_B_TEXT = 'Мой профиль'

    def __init__(self, bot_event: UserEvent):
        self.bot_event = bot_event
        self._chat_id = bot_event.message.chat.id



        # self.buttons = [
        #     KeyboardButton('💬', self.get_active_preset_name(), UIHandler.Command.show_preset_info),
        #     KeyboardButton('🟢', 'Включить контекст', UIHandler.Command.enable_gpt_context)
        # ]

    def create_menu(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        preset_info_button = types.KeyboardButton(f"{self.buttons[0].id} {self.buttons[0].text}")
        markup.row(preset_info_button)
        # context_button = types.KeyboardButton(f"{self.buttons[0].id} {self.buttons[0].text}")
        self.bot.send_message(self.message.chat.id, "Клавиатура создана", reply_markup=markup)


        # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # button1 = types.KeyboardButton(f"{self.__class__.PRESET_INFO_BUTTON_ID} {self.get_active_preset_name()}")
        # markup.row(button1)
        # button2 = types.KeyboardButton(f"{self.__class__.CREATE_PRESET_BUTTON_ID} {self.__class__.CREATE_PRESET_B_TEXT}")
        # button3 = types.KeyboardButton(f"{self.__class__.CHOOSE_PRESET_BUTTON_ID} {self.__class__.CHOOSE_PRESET_B_TEXT}")
        # button4 = types.KeyboardButton(f"{self.__class__.REMOVE_PRESET_BUTTON_ID} {self.__class__.REMOVE_PRESET_B_TEXT}")
        # button5 = types.KeyboardButton(f"{self.__class__.ENABLE_CONTEXT_BUTTON_ID} {self.__class__.ENABLE_CNTXT_B_TEXT}")
        # button6 = types.KeyboardButton(f"{self.__class__.STAT_BUTTON_ID} {self.__class__.STAT_B_TEXT}")
        # markup.add(button2, button3, button4, button5, button6)

    def handle_keyboard_event(self):
        for button in self.buttons:
            if button.id == self.message.text.split()[0]:
                button.callback(self.bot_event)

    def is_keyboard_event(self):
        msg_txt = self.message.text
        if not msg_txt or ' ' not in msg_txt:
            return False
        possible_button = self.message.text.split()[0]
        for button in self.buttons:
            if button.id.strip() == possible_button.strip():
                return True


    def get_active_preset_name(self):
        active_preset = self.user.config.load()["active_preset"]
        return next(iter(active_preset))


# Для прямых тестов
if __name__ == '__main__':
    pass
