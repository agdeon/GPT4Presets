import os
import json


class BotConfig:
    FILE_NAME = 'botconfig.cfg'

    CFG_DEFAULT_DICT = {
        "white_list_enabled": True,
        "white_list": [2124452396, 470286929],
        "black_list": [],
        "ranks":
            {
                "basic": {
                    "daily_tokens_limit": 4000,
                    "history_tokens_limit": 0,
                    "history_messages_limit": 0
                },
                "plus": {
                    "daily_tokens_limit": 20000,
                    "history_tokens_limit": 500,
                    "history_messages_limit": 5
                },
                "vip": {
                    "daily_tokens_limit": 40000,
                    "history_tokens_limit": 1000,
                    "history_messages_limit": 10
                },
                "admin": {
                    "daily_tokens_limit": 40000,
                    "history_tokens_limit": 1000,
                    "history_messages_limit": 10
                }
            }
    }

    @classmethod
    def get(cls) -> dict:
        if not os.path.exists(cls.FILE_NAME):
            cls._init()
        with open(cls.FILE_NAME, 'r') as cfg_file:
            cfg_dict = json.load(cfg_file)
        return cfg_dict

    @classmethod
    def write(cls, cfg_dict):
        with open(cls.FILE_NAME, 'w', encoding='utf-8') as file:
            json.dump(cfg_dict, file, indent=4, ensure_ascii=False)

    @classmethod
    def _init(cls):
        if not os.path.exists(cls.FILE_NAME):
            with open(cls.FILE_NAME, 'w', encoding='utf-8') as file:
                json.dump(cls.CFG_DEFAULT_DICT, file, indent=4, ensure_ascii=False)
            cls.write(cfg_dict=cls.CFG_DEFAULT_DICT)


# Пример использования
if __name__ == '__main__':
    cfg = BotConfig.get()
    cfg["ranks"]["basic"]["daily_tokens_limit"] = 50000
    BotConfig.write(cfg)

