import logging as log
import telebot
from telebot import types
from utils import questionnaire
from utils.storage.base import BaseStorage


def ask_question(uid: str, bot: telebot.TeleBot, storage: BaseStorage) -> None:
    log.debug(f"Asking {uid} question")
    name, question = questionnaire.pick_question()
    storage.set(uid, name)
    log.debug(f"Stored question {name} for {uid}")

    buttons = question["options"]
    markup = types.ReplyKeyboardMarkup(row_width=1)
    buttons = [types.KeyboardButton(button) for button in buttons]
    markup.add(*buttons)

    if "question" in question:
        log.debug(f"Sending text question to {uid}")
        bot.send_message(uid, question["question"], reply_markup=markup)
    else:
        log.debug(f"Sending img question to {uid}")
        caption = question.get("question", None)
        with open(question["image"], "rb") as img:
            bot.send_photo(uid, img, reply_markup=markup, caption=caption)


def _check_answer(uid: str, answer: str, storage: BaseStorage) -> tuple[bool, str]:
    """
    :raises KeyError: in case if storage does not containt current question for user
    """
    log.debug(f"Checking if {uid} provided a correct answer")
    q = storage.get(uid)
    correct_answer = questionnaire.get_answer(q)
    log.debug(f"{uid} provided `{answer}`; correct one is `{correct_answer}`")
    return (answer == correct_answer, correct_answer)


def check_answer(uid: str, answer: str, bot: telebot.TeleBot, storage: BaseStorage, phrases: dict[str, str]):
    success, correct = _check_answer(uid, answer, storage)
    msg = phrases["correct"] if success else f"{phrases['incorrect']} {correct}"
    log.debug(f"Sending results of {uid} answer")
    bot.send_message(
        uid,
        msg,
        reply_markup=types.ReplyKeyboardRemove(selective=False),
    )


def report_missing_user(uid: str, bot: telebot.TeleBot, phrases: dict[str, str]) -> None:
    log.warn(f"Something went wrong, reporting to {uid}")
    bot.send_message(
        uid,
        phrases["could_not_find_current_q"],
        reply_markup=types.ReplyKeyboardRemove(selective=False),
    )
