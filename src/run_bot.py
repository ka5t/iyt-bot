import argparse
import logging
import os
import signal
import sys
import telebot
import traceback
from utils import config
from utils import exceptions
from utils.storage.base import BaseStorage
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


def _edit_message(bot: telebot.TeleBot, call, text: str) -> None:
    msg_is_photo = call.message.text is None

    if msg_is_photo:
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=f"{call.message.caption}\n\n{text}",
            reply_markup=None,
            parse_mode="Markdown",
        )
    else:
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{call.message.text}\n\n{text}", reply_markup=None, parse_mode="Markdown"
        )


def _process_message(uid: str, answer: str, bot: telebot.TeleBot, storage: BaseStorage, phrases: dict[str, str]) -> None:
    try:
        iyt_bot.check_answer(uid, answer, bot, storage, phrases)
    except (KeyError, exceptions.CouldNotFindQuestionForUser):
        iyt_bot.report_missing_user(uid, bot, phrases)
    iyt_bot.ask_question(uid, bot, storage, conf.keyboard_type)


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
        iyt_bot.ask_question(msg.chat.id, bot, storage, conf.keyboard_type)

    @bot.message_handler(content_types=["text"])
    def handle_message(msg):
        log.debug(f"Handling msg {msg}")
        _process_message(msg.chat.id, msg.text, bot, storage, phrases)

    @bot.callback_query_handler(func=lambda call: True)
    def handle_inline_answer(call):
        log.debug(f"Handling inline {call}")
        _edit_message(bot, call, f"`> {phrases['your_inline_choice_was']} {call.data}`")
        _process_message(call.from_user.id, call.data, bot, storage, phrases)

    def handle_signals(signum: int, frame):
        log.debug(f"Handling signal {signum}")
        dump = storage.save()
        log.info(f"Database was saved to {dump}")
        if signum != signal.SIGUSR2:
            log.info("Stopping bot.")
            exit(0)

    signal.signal(signal.SIGTERM, handle_signals)
    signal.signal(signal.SIGHUP, handle_signals)
    signal.signal(signal.SIGINT, handle_signals)
    signal.signal(signal.SIGUSR2, handle_signals)

    while True:
        try:
            log.info("Starging bot")
            bot.polling(none_stop=True)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.error(str(exc_value) + repr(traceback.extract_tb(exc_traceback)))
