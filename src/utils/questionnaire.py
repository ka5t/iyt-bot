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


def get_answer(question_path: str, questions_dir: str = QUESTIONS_DIR) -> str:
    return _get_question(question_path, questions_dir)["correct"]
