import argparse
import logging
import os
import signal
import sys
import telebot
import traceback
from utils import config
from utils.storage.memory import NaiveStorage
from utils import iyt_bot
from utils import lang_pack

CONFIG_PATH = "config.yaml"
STORAGE_TYPES = {"memory": NaiveStorage}

logging.basicConfig()
log = logging.getLogger()
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
log.setLevel(LOGLEVEL)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start bot")
    parser.add_argument("--config", dest="config_file", default=CONFIG_PATH, help="Path to config file")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    conf = config.Config(args.config_file)
    log.debug(f"Set config: {conf}")

    storage = STORAGE_TYPES[conf.cache_type]()
    try:
        log.debug("Trying to load database..")
        storage.load()
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        log.warning(f"Could not load data from DB: {exc_value} {traceback.extract_tb(exc_traceback)}")
    phrases = lang_pack.phrases[conf.lang]

    bot = telebot.TeleBot(conf.token)
    log.debug("Bot initialized")

    @bot.message_handler(commands=["start"])
    def send_welcome(msg):
        bot.send_message(msg.chat.id, phrases["greeting"])
        iyt_bot.ask_question(msg.chat.id, bot, storage)

    @bot.message_handler(content_types=["text"])
    def handle_message(msg):
        try:
            iyt_bot.check_answer(msg.chat.id, msg.text, bot, storage, phrases)
        except KeyError:
            iyt_bot.report_missing_user(msg.chat.id, bot, phrases)
        iyt_bot.ask_question(msg.chat.id, bot, storage)

    def shutdown(signum, frame):
        dump = storage.save()
        log.info(f"Stopping bot. Database was saved to {dump}")
        exit(0)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGHUP, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    while True:
        try:
            log.info("Starging bot")
            bot.polling(none_stop=True)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error(str(exc_value) + repr(traceback.extract_tb(exc_traceback)))
