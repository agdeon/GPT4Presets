import json
import logging
import os
import shutil
import time
import copy
from typing import Union
from datetime import datetime

from bot_config import BotConfig


class Ranks:
    """
    Класс для настроек рангов пользователей класса User
    Обязателен к импорту наряду с ним
    """
    BASIC = 'basic'
    PLUS = 'plus'
    VIP = 'vip'
    ADMIN = 'admin'


class UserDefaults:
    """
    Класс для настроек поведения класса User
    Обязателен к импорту наряду с ним
    """
    FOLDER_NAME = "users"
    LOG_FILENAME = 'user.log'
    HISTORY_FILENAME = 'gpt_history.json'
    CFG_FILENAME = 'user.cfg'
    STAT_FILENAME = 'gpt_request_stats.json'
    LANGUAGE = 'ru'
    RANK = Ranks.BASIC


class User:
    """
    Класс для управления записями пользователей, регистрации, сохранения истории,
    конфигурации, логов и тд.
    """
    CONSOLE_LOG_LVL = logging.DEBUG
    FILE_LOG_LVL = logging.INFO
    DEFAULT_SYS_CONTENT = {"role": "system", "content": ""}

    def __init__(self, chat_id):

        chat_id = str(chat_id)
        self.id = chat_id

        self.folder_name = chat_id  # may change later
        self._user_folder_path = os.path.join(UserDefaults.FOLDER_NAME, self.folder_name)
        self._create_users_folder()
        if self.is_new_user():
            self._create_user_folder()

        # Instances of internal classes
        self.config = self.Config(self)
        self.gpt_history = self.GptHistory(self)
        self.logger = self.Logger(self)
        self.stats = self.Stats(self)

    def set_gpt_prompt(self, prompt_text):
        hst = self.get_history()
        system_content = hst[0]
        if 'role' not in system_content or  system_content['role'] != 'system':
            self.error(f"Ошибка в функции set_gpt_prompt: 'role' not in system_content or  system_content['role'] != 'system'")
        hst[0]['content'] = prompt_text
        self.save_history(hst)

    def reset(self):
        files_to_delete = [
            self.logger._filepath,
            self.gpt_history._filepath,
            self.config._filepath
        ]
        self.logger.unbind_handlers()
        for path in files_to_delete:
            if os.path.exists(path):
                os.remove(path)
        self.config = self.Config(self)
        self.gpt_history = self.GptHistory(self)
        self.logger = self.Logger(self)

    def is_new_user(self):
        user_path = os.path.join(UserDefaults.FOLDER_NAME, self.id)
        if not os.path.exists(user_path):
            return True

    @classmethod
    def _create_users_folder(cls):
        main_folder = UserDefaults.FOLDER_NAME
        if not os.path.exists(main_folder):
            os.makedirs(main_folder)

    @staticmethod
    def read_json_from_file(path) -> Union[dict, list]:
        with open(path, 'r', encoding='utf-8') as file:
            json_content = json.load(file)
        return json_content

    @staticmethod
    def write_json_to_file(path, json_content: Union[dict, list]):
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(json_content, file, indent=4, ensure_ascii=False)

    def _create_user_folder(self):
        user_path = self._user_folder_path
        if not os.path.exists(user_path):
            os.makedirs(user_path)

    ############################################
    # Inner classes #################################
    #######################################################
    class Logger:
        FILENAME = UserDefaults.LOG_FILENAME

        def __init__(self, user_instance):
            self.user_instance = user_instance
            self._filepath = os.path.join(UserDefaults.FOLDER_NAME, self.user_instance.id, self.FILENAME)
            self._init()

            self._logger = logging.getLogger('USER_' + self.user_instance.id)
            self._configure_logger()

        def debug(self, text):
            self._logger.debug(text)

        def info(self, text):
            self._logger.info(text)

        def error(self, text):
            self._logger.error(text)

        def unbind_handlers(self):
            logger = self._logger
            for handler in logger.handlers[:]:  # Итерируем по копии списка, чтобы безопасно удалять
                if isinstance(handler, logging.FileHandler):  # Проверяем, является ли обработчик FileHandler
                    logger.removeHandler(handler)
                    handler.close()

        def _init(self):
            if not os.path.exists(self._filepath):
                with open(self._filepath, 'w', encoding='utf-8') as file:
                    pass # пустой

        def _configure_logger(self):
            self._logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            console_handler = logging.StreamHandler()
            console_handler.setLevel(User.CONSOLE_LOG_LVL)
            console_handler.setFormatter(formatter)

            file_handler = logging.FileHandler(self._filepath, encoding='utf-8')
            file_handler.setLevel(User.FILE_LOG_LVL)
            file_handler.setFormatter(formatter)

            self._logger.addHandler(console_handler)
            self._logger.addHandler(file_handler)

    class GptHistory:
        FILENAME = UserDefaults.HISTORY_FILENAME
        DEFAULT_MSG = {"role": "system", "content": ""}

        def __init__(self, user_instance):
            self.user_instance = user_instance
            self._filepath = os.path.join(UserDefaults.FOLDER_NAME, self.user_instance.id, self.__class__.FILENAME)
            self._init()

        def load(self) -> list:
            return self.user_instance.read_json_from_file(self._filepath)

        def write(self, hist_list):
            if hist_list[0]['role'] != 'system':
                hist_list.insert(0, self.__class__.DEFAULT_MSG)
            user_rank = self.user_instance.config.load()["rank"]
            user_history_limit = int(BotConfig.load()["ranks"][user_rank]["history_messages_limit"])
            while len(hist_list) > user_history_limit and len(hist_list) > 1:
                hist_list.pop(1)  # Удаляем второй элемент чтобы освободить место с конца но и оставить инструкцию (0)
            self.user_instance.write_json_to_file(self._filepath, hist_list)

        def _init(self):
            if not os.path.exists(self._filepath):
                User.write_json_to_file(self._filepath, self.DEFAULT_MSG)

    class Config:
        FILENAME = UserDefaults.CFG_FILENAME
        DEFAULT_VAL = {
            "id": None,
            "language": UserDefaults.LANGUAGE,
            "rank": UserDefaults.RANK,
            "is_admin": False,
            "is_blocked": False,
            "default_preset": {"Обычный чат GPT": ""},
            "active_preset": {"Обычный чат GPT": ""},
            "instruction_presests": {
                "Обычный чат GPT": "",
                "Лаконичный чат GPT": "Отвечай коротко и по делу. Без воды, минимум текста.",
                "Точная статистика": "Твои ответы должны содержать подробную статистику и цифры. В удобном для понимания виде."
            },
        }

        def __init__(self, user_instance):
            self.user_instance = user_instance  # Сохраняем ссылку на User
            self._filepath = os.path.join(UserDefaults.FOLDER_NAME, self.user_instance.id, self.__class__.FILENAME)
            self._init()

        def load(self) -> Union[dict, list]:
            return self.user_instance.read_json_from_file(self._filepath)

        def write(self, cfg_dict: Union[dict, list]):
            return self.user_instance.write_json_to_file(self._filepath, cfg_dict)

        def _init(self):
            if not os.path.exists(self._filepath):
                self.__class__.DEFAULT_VAL["id"] = self.user_instance.id
                self.user_instance.write_json_to_file(self._filepath, self.DEFAULT_VAL)

    class Stats:
        FILENAME = UserDefaults.STAT_FILENAME
        DEFAULT_VAL = {
            "total_requests": 0,
            "total_tokens_spent": 0,
            "total_cost": 0,
            "today_requests": 0,
            "today_tokens_spent": 0,
            "today_cost": 0,
            "last_request_date": "2020-01-31"
        }

        def __init__(self, user_instance):
            self.user_instance = user_instance  # Сохраняем ссылку на User
            self._filepath = os.path.join(UserDefaults.FOLDER_NAME, self.user_instance.id, UserDefaults.STAT_FILENAME)
            self._init()

        def load(self) -> Union[dict, list]:
            return self.user_instance.read_json_from_file(self._filepath)

        def write(self, stats_dict: Union[dict, list]):
            return self.user_instance.write_json_to_file(self._filepath, stats_dict)

        def _init(self):
            if not os.path.exists(self._filepath):
                self.user_instance.write_json_to_file(self._filepath, self.DEFAULT_VAL)
            if self._is_next_day():
                self._reset_today_stats()

        def _reset_today_stats(self):
            today_stat_keys = ["today_requests", "today_tokens_spent", "today_cost"]
            stats = self.load()
            for key in today_stat_keys:
                stats[key] = 0
            self.write(stats)

        def _is_next_day(self):
            stats = self.load()
            last_req_date = int(stats["last_request_date"].replace("-", ""))
            today_date = int(str(datetime.now().date()).replace("-", ""))
            return today_date > last_req_date

# For direct module tests
if __name__ == '__main__':
    test_conv_hist = [
        {"role": "user", "content": "Пример запроса пользователя"},
        {"role": "assistant", "content": "Пример ответа ИИ"}
    ]

    user = User('41242')
    cfg = user.config.load()
    cfg["rank"] = Ranks.VIP
    user.logger.info(f"Ранг пользователя {user.id} изменен на {Ranks.VIP}")
    user.config.write(cfg)
    user.gpt_history.write(test_conv_hist * 100)
    new_stats = user.stats.load()
    new_stats["today_tokens_spent"] = 1312
    user.stats.write(new_stats)

