import msgspec
from datetime import datetime
from typing import Optional
from ..questionnaires import Questionnaire


class UserQuestionnaireSession(msgspec.Struct, kw_only=True):
    id: int
    questionnaire: Questionnaire
    status: str
    current_ordering: int
    is_finished: bool
    started_at: datetime
    reply_text: Optional[str]
    finished_at: Optional[datetime]