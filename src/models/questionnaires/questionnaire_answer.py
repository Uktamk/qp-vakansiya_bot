import msgspec

class QuestionnaireAnswer(msgspec.Struct, kw_only=True):
    ordering: int
    text: str
    is_correct: bool