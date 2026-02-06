from .base import BaseApiException

class UserDoesNotExistError(BaseApiException):
    pass

class QuestionnaireDoesNotExist(BaseApiException):
    pass