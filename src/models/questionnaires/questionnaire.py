import msgspec
from typing import List, Optional
from .questionnaire_answer import QuestionnaireAnswer


class Questionnaire(msgspec.Struct, kw_only=True):
    id: int
    ordering: int
    question: str
    incorrect_answer_text: Optional[str]
    answers: List[QuestionnaireAnswer]
