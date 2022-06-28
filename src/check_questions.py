import os

from utils import questionnaire

IMGS_DIR = "resources/imgs/"

class QuestionsCheckError(Exception):
    """Base class for custom exceptions"""
    pass

class BothQuestionAndImageError(QuestionsCheckError):
    """Raised when both `question` and `image` fields are presented in the file"""
    pass

class CorrectOptionsMissmatchError(QuestionsCheckError):
    """Raised when there are less than 2 options in the file"""
    pass

class NotEnoughOptionsError(QuestionsCheckError):
    """Raised when there are less than 2 options in the file"""
    pass

class ImageNotFoundError(QuestionsCheckError):
    """Raised when mentioned image was not found in imgs directory"""
    pass

if __name__ == '__main__':
    errors = []
    for q in questionnaire._list_questions():
        try:
            data = questionnaire._get_question(q)
            if "image" in data:
                if "question" in data:
                    raise BothQuestionAndImageError()
                if not os.path.exists(os.path.join(IMGS_DIR, data["image"])):
                    raise ImageNotFoundError()
            if len(data["options"]) < 2:
                raise NotEnoughOptionsError()
            if not data["correct"] in data["options"]:
                raise CorrectOptionsMissmatchError()
        except Exception as e:
            errors.append((q, f"Could not parse - {e}"))

    if len(errors) == 0:
        print("Tests succeeded")
    else:
        for f, err in errors:
            print(f"{f} - {err}")
        exit(1)
