from user import User
import json
from telebot import types





class ButtonManager:
    """
        Статичное меню
        💬 Обычный GPT
        🟢 Включить контекст
        📑 Выбрать пресет
        ➕ Создать пресет
        🗑 Удалить пресет
        📊 Статистика
    """

    # Все markup кнопки будут идентифицироваться по emoji
    PRESET_INFO_BUTTON_ID = '💬' # у этой кнопки будет динамическое название в зависимости от пресета

    ENABLE_CONTEXT_BUTTON_ID = '🟢' # кнопки контекста будут сменяться одна на другую
    ENABLE_CNTXT_B_TEXT = "Включить контекст"

    DISABLE_CONTEXT_BUTTON_ID = '🔴' # кнопки контекста будут сменяться одна на другую
    DISABLE_CNTXT_B_TEXT = "Выключить контекст"

    CHOOSE_PRESET_BUTTON_ID = '📑'
    CHOOSE_PRESET_B_TEXT = 'Выбрать пресет'

    CREATE_PRESET_BUTTON_ID = '➕'
    CREATE_PRESET_B_TEXT = 'Создать пресет'

    REMOVE_PRESET_BUTTON_ID = '🗑️'
    REMOVE_PRESET_B_TEXT = 'Удалить пресет'

    STAT_BUTTON_ID = '📊'
    STAT_B_TEXT = 'Статистика'

    def __init__(self, user: User):
        self._user = user
        self._chat_id = user.id
        self._cfg_path = f"{User.USERS_FOLDER_NAME}/{self._user.user_folder_name}/{User.USER_CFG_FN}"

        self._ensure_active_preset()

    def create_menu(self) -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(f"{self.__class__.PRESET_INFO_BUTTON_ID} {self.get_active_preset_name()}")
        markup.row(button1)
        button2 = types.KeyboardButton(f"{self.__class__.ENABLE_CONTEXT_BUTTON_ID} {self.__class__.ENABLE_CNTXT_B_TEXT}")
        button3 = types.KeyboardButton(f"{self.__class__.CHOOSE_PRESET_BUTTON_ID} {self.__class__.CHOOSE_PRESET_B_TEXT}")
        button4 = types.KeyboardButton(f"{self.__class__.CREATE_PRESET_BUTTON_ID} {self.__class__.CREATE_PRESET_B_TEXT}")
        button5 = types.KeyboardButton(f"{self.__class__.REMOVE_PRESET_BUTTON_ID} {self.__class__.REMOVE_PRESET_B_TEXT}")
        button6 = types.KeyboardButton(f"{self.__class__.STAT_BUTTON_ID} {self.__class__.STAT_B_TEXT}")
        markup.add(button2, button3, button4, button5, button6)
        return markup

    def get_active_preset_name(self):
        active_preset = self.get_active_preset()
        self._user.info(f"get_active_preset_name(), active_preset= {active_preset}")
        first_key = next(iter(active_preset))
        self._user.info(f"get_active_preset_name(), first_key= {first_key}")
        return first_key

    def get_active_preset(self):
        self._user.info("_cfg_path = " + self._cfg_path)
        with open(self._cfg_path, 'r', encoding='utf-8') as file:
            cfg = json.load(file)
        preset = cfg.load("active_preset", None)
        self._user.info(f"preset = {preset}")
        if not preset:
            error_txt = "Ошибка в функции _ensure_active_preset: отсутсвуют пресеты пользователя"
            self._user.error(error_txt)
            raise Exception(error_txt)
        return preset

    def _ensure_active_preset(self):
        with open(self._cfg_path, 'r', encoding='utf-8') as file:
            cfg = json.load(file)
        active_preset = cfg.load("active_preset", None)

        if not active_preset:
            default_preset = cfg.load("default_preset", None)
            if not default_preset:
                error_txt = "Ошибка в функции _ensure_active_preset: отсутсвуют пресеты пользователя"
                self._user.error(error_txt)
                raise Exception(error_txt)

            cfg["active_preset"] = default_preset
            with open(self._cfg_path, 'w', encoding='utf-8') as config_file:
                json.dump(cfg, config_file, indent=4, ensure_ascii=False)

        # first_preset_name = _get_first_key_in_instruction_presets()
        # with open(self._cfg_path, 'w',
        #           encoding='utf-8') as config_file:
        #     json.dump(def_user_cfg, config_file, indent=4, ensure_ascii=False)
        # return first_preset_name


# Для прямых тестов
if __name__ == '__main__':
    pass