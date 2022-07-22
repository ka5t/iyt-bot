import logging as log
import telebot
from telebot import types
from utils import questionnaire
from utils import exceptions
from utils.storage.base import BaseStorage


def reply_keyboard(options: list[str]) -> types.ReplyKeyboardMarkup:
    row_width = 2 if max([len(str(x)) for x in options]) < 72 else 1
    markup = types.ReplyKeyboardMarkup(row_width=row_width)
    buttons = [types.KeyboardButton(option) for option in options]
    markup.add(*buttons)
    return markup


def inline_keyboard(options: list[str]) -> types.InlineKeyboardMarkup:
    row_width = 2 if max([len(str(x)) for x in options]) < 25 else 1
    markup = types.InlineKeyboardMarkup(row_width=row_width)
    buttons = [types.InlineKeyboardButton(option, callback_data=option) for option in options]
    markup.add(*buttons)
    return markup


KEYBOARDS = {
    "inline": inline_keyboard,
    "reply": reply_keyboard,
}


def ask_question(uid: str, bot: telebot.TeleBot, storage: BaseStorage, keyboardType: str = "inline") -> None:
    log.debug(f"Asking {uid} question")
    try:
        weights = storage.get(f"stats_{uid}")
    except KeyError:
        log.warning(f"User {uid} has no history")
        weights = {}
    name, question = questionnaire.pick_weighted_question(weights=weights)
    storage.set(uid, name)
    log.debug(f"Stored question {name} for {uid}")

    markup = KEYBOARDS[keyboardType]([str(o) for o in question["options"]])

    if "image" in question:
        log.debug(f"Sending img question to {uid}")
        caption = question.get("question", None)
        with open(question["image"], "rb") as img:
            bot.send_photo(uid, img, reply_markup=markup, caption=caption)
    else:
        log.debug(f"Sending text question to {uid}")
        bot.send_message(uid, question["question"], reply_markup=markup)


def _check_answer(uid: str, answer: str, storage: BaseStorage) -> tuple[bool, str, str]:
    """
    :raises KeyError: in case if storage does not containt current question for user
    """
    log.debug(f"Checking if {uid} provided a correct answer")
    q = storage.get(uid)
    correct_answer = str(questionnaire.get_answer(q))
    log.debug(f"{uid} provided `{answer}`; correct one is `{correct_answer}`")
    return (answer == correct_answer, q, correct_answer)


def _increment_stats(uid: str, q: str, storage: BaseStorage) -> None:
    score = 1
    user_stats = {}
    try:
        user_stats = storage.get(f"stats_{uid}")
        score += user_stats[q]
    except KeyError:
        pass
    log.debug(f"User {uid} answered correctly on {q}, new score is {score}")
    user_stats[q] = score
    storage.set(f"stats_{uid}", user_stats)


def check_answer(uid: str, answer: str, bot: telebot.TeleBot, storage: BaseStorage, phrases: dict[str, str]):
    try:
        log.debug(f"Checkin {answer}")
        success, q, correct = _check_answer(uid, answer, storage)
        if success:
            msg = phrases["correct"]
            _increment_stats(uid, q, storage)
        else:
            msg = f"{phrases['incorrect']} {correct}"
        log.debug(f"Sending results of {uid} answer")
        bot.send_message(
            uid,
            msg,
            reply_markup=types.ReplyKeyboardRemove(selective=False),
        )
    except FileNotFoundError:
        raise exceptions.CouldNotFindQuestionForUser("Could not find question for {uid}")


def report_missing_user(uid: str, bot: telebot.TeleBot, phrases: dict[str, str]) -> None:
    log.warn(f"Something went wrong, reporting to {uid}")
    bot.send_message(
        uid,
        phrases["could_not_find_current_q"],
        reply_markup=types.ReplyKeyboardRemove(selective=False),
    )
