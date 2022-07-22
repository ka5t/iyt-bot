import logging as log
import os
import random
import typing
import yaml

QUESTIONS_DIR = "resources/questions/"
IMGS_DIR = "resources/imgs/"


def _list_questions(questions_dir: str = QUESTIONS_DIR) -> list[str]:
    return [x for x in os.listdir(questions_dir) if x.endswith(".yml")]


def _pick_question(questions_dir: str = QUESTIONS_DIR) -> str:
    return random.choice(_list_questions(questions_dir))


def _get_question(question_path: str, questions_dir: str = QUESTIONS_DIR) -> dict[str, typing.Any]:
    with open(os.path.join(questions_dir, question_path), "r") as f:
        data = yaml.safe_load(f)
    if "image" in data:
        data["image"] = os.path.join(IMGS_DIR, data["image"])
    return data


def pick_question(questions_dir: str = QUESTIONS_DIR) -> tuple[str, dict[str, typing.Any]]:
    q = _pick_question(questions_dir)
    return (q, _get_question(q))


def pick_weighted_question(questions_dir: str = QUESTIONS_DIR, weights: dict[str, int] = {}) -> tuple[str, dict[str, typing.Any]]:
    # more weight question has - less chance to pick it up
    if len(weights) == 0:
        return pick_question(questions_dir)
    pool = _list_questions(questions_dir)
    lowest_weight = 9999999999999.0  # TODO: refactor it :)
    for q in pool:
        weight = random.random() * (weights.get(q, 0) + 1)
        if weight < lowest_weight:
            log.debug(f"New lowest {weight=}; {q=}")
            lowest_weight = weight
            chosen_q = q
    return (chosen_q, _get_question(chosen_q))


def get_answer(question_path: str, questions_dir: str = QUESTIONS_DIR) -> str:
    return _get_question(question_path, questions_dir)["correct"]
