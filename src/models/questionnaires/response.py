import msgspec


class AnswerResponse(msgspec.Struct, kw_only=True):
    message: str
    ok: bool
    status_code: str
    reply_text: str | msgspec.UnsetType = msgspec.UNSET
    next_questionnaire: int | msgspec.UnsetType = msgspec.UNSET
