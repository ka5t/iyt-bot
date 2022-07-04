import os
import yaml


class Config:
    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            conf = yaml.safe_load(f)

        self.token = os.getenv("BOT_TOKEN", conf["bot_token"])
        self.cache_type = os.getenv("BOT_STORAGE_TYPE", conf["bot_storage_type"])
        self.lang = os.getenv("BOT_LANGUAGE", conf["bot_language"])
        self.keyboard_type = os.getenv("BOT_KEYBOARD_TYPE", conf["bot_keyboard_type"])
