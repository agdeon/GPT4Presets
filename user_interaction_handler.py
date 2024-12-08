import telebot
from user import User


# Любое событие должно быть создано через этот класс
class UserEvent:
    def __init__(self, bot: telebot.TeleBot, message: telebot.types.Message, user: User):
        self.bot = bot
        self.message = message
        self.user = user

    def is_keyboard_event(self):
        pass


class UIHandler:

    class Command:
        @staticmethod
        def show_preset_info(bot_event: UserEvent):
            bot = bot_event.bot
            user_id = bot_event.message.chat.id
            bot.send_message(user_id, "Some info bout preset")

        @staticmethod
        def enable_gpt_context(bot_event: UserEvent):
            pass

    class Keyboard:
        pass