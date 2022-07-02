class IYTBotException(Exception):
    """Base class for custom exceptions"""

    pass


class CouldNotFindQuestionForUser(IYTBotException):
    """
    Raised when questionnaire does not contain specific question.
    This might happen if some files were renamed while user had an active question
    """

    pass
