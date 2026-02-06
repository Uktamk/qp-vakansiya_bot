import msgspec
from datetime import datetime
from typing import Optional


class UserQuestionnaireSession(msgspec.Struct, kw_only=True):
    id: int
    questionnaire: int
    status: str
    current_ordering: int
    is_finished: bool
    started_at: datetime
    reply_text: Optional[str]
    finished_at: Optional[datetime]