import os
import random
import typing
import yaml

QUESTIONS_DIR = "resources/questions/"


def _list_questions(questions_dir: str = QUESTIONS_DIR) -> list[str]:
    return [x for x in os.listdir(questions_dir) if x.endswith(".yml")]


def _pick_question(questions_dir: str = QUESTIONS_DIR) -> str:
    return random.choice(_list_questions(questions_dir))


def _get_question(question_path: str) -> dict[str, typing.Any]:
    with open(os.path.join(QUESTIONS_DIR, question_path), "r") as f:
        data = yaml.safe_load(f)
    return data


def pick_question(questions_dir: str = QUESTIONS_DIR) -> tuple[str, dict[str, typing.Any]]:
    q = _pick_question(questions_dir)
    return (q, _get_question(q))
